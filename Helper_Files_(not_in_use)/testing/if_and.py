def test_1(a):
    if a < 5:
        print(f"nice! :)")
    else:
        print("TOO BIG!!!")

def test_2(b):
    if 2 <= b and b <= 5:
        print(f"{b} in [2..5]")
    else:
        print("Outside...")


if __name__ == '__main__':
    test_1(2)
    test_1(6)

    print("\n\n")

    test_2(1)
    test_2(3)
    test_2(6)
