from streamlit.testing.v1 import AppTest


def test_streamlit_app_renders_without_exception():
    app = AppTest.from_file("app.py").run(timeout=30)

    assert not app.exception
    assert app.title or app.markdown
    assert app.button[0].label == "Estimate asking price"
