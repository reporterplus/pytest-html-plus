def test_example_com(page):
    # `page` is provided by pytest-playwright
    page.goto("https://example.com")
    assert "Example Domain" in page.content()
