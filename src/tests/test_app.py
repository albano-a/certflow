from streamlit.testing.v1 import AppTest


def test_app_runs_and_renders_title():
    at = AppTest.from_file("src/app.py")
    at.run()
    assert not at.exception, f"App raised an exception: {at.exception}"

    # Check that the main title is present
    titles = [el.value for el in at.title]
    assert "Gerador de Certificados" in titles
