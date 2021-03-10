from fns.decorators import batched


def test_batched():
    @batched(8)
    def echo(x):
        return [e * 2 for e in x]

    assert echo(range(16)) == [e * 2 for e in range(16)]
