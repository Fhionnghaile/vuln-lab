"""Derry-Vuln-Lab: deliberately vulnerable Flask app.

One app, two modes: create_app(secure=False) is the vulnerable "main"; create_app(secure=True)
is the remediated "fixed" branch. The test suite runs BOTH and proves each flaw is exploitable in
one and closed in the other. Every PoC is hard-wired to this lab's own routes (nothing reusable).
"""
from __future__ import annotations
import hashlib, html, sqlite3
import bcrypt, jwt
from flask import Flask, request, jsonify, g

JWT_SECRET = "s3cr3t-signing-key-change-me-0123456789abcdef"
ALLOWED_FETCH_HOSTS = {"example.com", "api.partner.test"}

def _db():
    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    con.executescript("""
        CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, ssn TEXT, role TEXT);
    """)
    con.execute("INSERT INTO users VALUES (1,'alice','alicepw','111-11-1111','user')")
    con.execute("INSERT INTO users VALUES (2,'bob','bobpw','222-22-2222','user')")
    con.execute("INSERT INTO users VALUES (3,'admin','adminpw','999-99-9999','admin')")
    return con

def create_app(secure: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["SECURE"] = secure

    @app.before_request
    def _conn():
        g.db = _db()

    # A01/A03 - SQL injection on login
    @app.post("/login")
    def login():
        u = request.json.get("username", ""); p = request.json.get("password", "")
        if secure:
            row = g.db.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
        else:
            row = g.db.execute(f"SELECT * FROM users WHERE username='{u}' AND password='{p}'").fetchone()  # noqa: S608
        if not row:
            return jsonify(error="bad credentials"), 401
        return jsonify(ok=True, user=row["username"], role=row["role"])

    # A01 Broken Access Control - IDOR
    @app.get("/api/user/<int:uid>")
    def get_user(uid: int):
        caller = request.headers.get("X-User-Id", type=int)
        if secure and caller != uid:
            return jsonify(error="forbidden"), 403
        row = g.db.execute("SELECT id,username,ssn FROM users WHERE id=?", (uid,)).fetchone()
        return (jsonify(dict(row)) if row else (jsonify(error="not found"), 404))

    # A03 Injection - reflected XSS
    @app.get("/greet")
    def greet():
        name = request.args.get("name", "guest")
        body = html.escape(name) if secure else name
        return f"<h1>Hello, {body}</h1>", 200, {"Content-Type": "text/html"}

    # A01 Broken Access Control - SSRF
    @app.get("/fetch")
    def fetch():
        from urllib.parse import urlparse
        host = urlparse(request.args.get("url", "")).hostname or ""
        if secure and host not in ALLOWED_FETCH_HOSTS:
            return jsonify(error="host not allowed"), 403
        return jsonify(fetched=host)  # lab stub: proves the access decision, does not egress

    # A07 Auth failures - JWT alg confusion / unverified
    @app.get("/admin")
    def admin():
        token = request.headers.get("Authorization", "").removeprefix("Bearer ")
        try:
            if secure:
                claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            else:
                claims = jwt.decode(token, options={"verify_signature": False})  # trusts anything
        except Exception:
            return jsonify(error="invalid token"), 401
        if claims.get("role") != "admin":
            return jsonify(error="forbidden"), 403
        return jsonify(secret="flag{admin-area}")

    # A02 Cryptographic failures - password storage
    @app.post("/register")
    def register():
        pw = request.json.get("password", "")
        stored = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode() if secure else hashlib.md5(pw.encode()).hexdigest()
        return jsonify(stored=stored, algorithm="bcrypt" if secure else "md5")

    return app

if __name__ == "__main__":
    create_app(secure=False).run(host="127.0.0.1", port=5000)
