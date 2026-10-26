import secrets
from string import ascii_letters, digits


def generate_random_slug(lenght: int = 6):
    """Generate a random slug of specified length."""
    characters = ascii_letters + digits
    return ''.join(secrets.choice(characters) for _ in range(lenght))

def test_generate_random_slug():
    """Unit test for generate_random_slug function."""
    slug = generate_random_slug(8)
    assert len(slug) == 8, "Slug length should be 8"
    assert all(c in ascii_letters + digits for c in slug), "Slug should only contain letters and digits"

if __name__ == "__main__":
    test_generate_random_slug()
    print("All tests passed.")