import os
from pathlib import Path
from typing import Iterable

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from markdown import markdown
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", BASE_DIR / "data" / "uploads"))
ALLOWED_MARKDOWN = {"md", "markdown"}
ALLOWED_IMAGES = {"png", "jpg", "jpeg", "gif", "svg"}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me")
app.config["UPLOAD_DIR"] = UPLOAD_DIR


def ensure_upload_dir() -> None:
    """Create the upload directory if it does not exist."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str, allowed: Iterable[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


@app.route("/")
def index():
    ensure_upload_dir()
    markdown_files = sorted(
        [f.name for f in UPLOAD_DIR.iterdir() if f.is_file() and allowed_file(f.name, ALLOWED_MARKDOWN)],
        key=str.lower,
    )
    return render_template("index.html", markdown_files=markdown_files)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    ensure_upload_dir()
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("请选择要上传的文件。", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        if allowed_file(filename, ALLOWED_MARKDOWN | ALLOWED_IMAGES):
            destination = UPLOAD_DIR / filename
            file.save(destination)
            flash(f"已成功上传 {filename}。", "success")
            return redirect(url_for("index"))

        flash("仅支持上传 Markdown 或常见图片文件。", "error")
        return redirect(request.url)

    return render_template("upload.html")


@app.route("/view/<path:filename>")
def view_markdown(filename: str):
    ensure_upload_dir()
    secure_name = secure_filename(filename)
    target = UPLOAD_DIR / secure_name
    if not target.is_file() or not allowed_file(secure_name, ALLOWED_MARKDOWN):
        abort(404)

    with target.open("r", encoding="utf-8") as fh:
        content = fh.read()

    html = markdown(
        content,
        extensions=["fenced_code", "tables", "toc", "codehilite", "nl2br"],
        output_format="html5",
    )
    return render_template("view.html", filename=secure_name, content=html)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    ensure_upload_dir()
    return send_from_directory(UPLOAD_DIR, filename)


if __name__ == "__main__":
    ensure_upload_dir()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=False)
