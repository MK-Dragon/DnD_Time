import time
import datetime


def t1():
    t_now = datetime.datetime.now()

    t_plus = t_now + datetime.timedelta(seconds=.5)
    t_minus = t_now - datetime.timedelta(seconds=.5)

    print(t_now)
    print(t_plus)
    print(t_minus)

    t_delta = t_plus - t_minus

    print(f"Delta: {t_delta}")


def get_client_time() -> datetime.datetime:
    return datetime.datetime.now()


def compere_time(time_client: datetime.datetime, threshold: float) -> bool:
    # get time:
    t_now = datetime.datetime.now()
    print(f"Server_Now: {t_now}")
    print(f"Client_time: {time_client}")

    t_plus = t_now + datetime.timedelta(seconds=threshold/2)
    t_minus = t_now - datetime.timedelta(seconds=threshold/2)
    print(f"Threshold: {t_minus} - {t_plus}")

    if t_minus <= time_client and time_client <= t_plus:
        print("OK - Within the threshold!")
        return True

    else:
        print("NOK")
        return False



if __name__ == '__main__':
    print("test 1:")
    t1()
    print("\n---//---\n")

    print("test 2:")
    time_clint = get_client_time()
    time.sleep(0.5)
    status = compere_time(time_clint, 1.2)
    print(f"Status: {status}")
