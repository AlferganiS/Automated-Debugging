def debug_main():
    def ackermann(m, n):
        if m == 0:
            return n + 1
        elif n == 0:
            return ackermann(m - 1, 1)
        else:
            return ackermann(m - 1, ackermann(m, n - 1))

    ackermann(2, 1)
    ackermann(3, 3)

if __name__ == '__main__':
    debug_main()
