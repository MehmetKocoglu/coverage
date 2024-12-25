class FaktoriyelCalculator:
    def rekursif(self, n):
        if n < 0:
            raise ValueError("Faktöriyel negatif sayılar için tanımlı değildir.")
        if n == 0 or n == 1:
            return 1
        return n * self.rekursif(n - 1)

    def basic(self, n):
        if n < 0:
            raise ValueError("Faktöriyel negatif sayılar için tanımlı değildir.")
        b = 1
        for i in range(1, n + 1):
            b *= i
        return b