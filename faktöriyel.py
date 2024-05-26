import unittest
n = 5
class a(unittest.TestCase):
    # Rekürsif faktöriyel hesaplama fonksiyonu
    def rekursif(self,n):
        if n == 0 or n == 1:
            return 1
        else:
            return n * self.rekursif(n - 1)
    # Normal faktöriyel hesaplama fonksiyonu
    #def basic(self,n):
     #   b = 1
      #  for i in range(1, n + 1):
       #     b *= i
        #return b

if __name__ == "__main__":
     unittest.main()
