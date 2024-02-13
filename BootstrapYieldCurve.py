import math


class BootstrapYieldCurve:

    def __init__(self):
        self.time_to_first_coupon_payment = 0
        self.face_value = 1000
        self.price = []
        self.coupon = []
        self.numbers_of_payments = []
        self.spot_rate = []
        self.time_values = []
        self.yield_values = []
        self.r_ti = 0
        self.forward_rates = []
        self.yield_log = []
        self.forward_log = []

    def add_data(self, face_value, T, coup, price, time_to_first_coupon_payment,
                 compounding_frequency=2):

        self.time_to_first_coupon_payment = time_to_first_coupon_payment
        self.price.append(1000 * price / 100)
        self.coupon.append(coup)
        self.numbers_of_payments.append(T)

    def get_r_t1(self):
        """first sorting the all the lists so that the numbers of payments is of
            ascending order, with price, coupon the corresponding index,
            then return the first term of spots rate (zero coupon bond)"""
        ind = self.numbers_of_payments.index(min(self.numbers_of_payments))
        sorted_lists = sorted(
            zip(self.numbers_of_payments, self.price, self.coupon),
            key=lambda x: x[0])
        self.numbers_of_payments, self.price, self.coupon = zip(*sorted_lists)
        self.numbers_of_payments = list(self.numbers_of_payments)
        self.price = list(self.price)
        self.coupon = list(self.coupon)
        a = -(math.log(
            (self.price[ind] + (0.5 - self.time_to_first_coupon_payment) *
             self.coupon[ind] * self.face_value)  # dirty price
            / self.face_value)  # notion price
              / self.time_to_first_coupon_payment)
        self.r_ti = a
        self.time_values.append(self.time_to_first_coupon_payment)
        return a

    def get_the_summation_part(self):
        a = 0
        for i in range(len(self.time_values)):
            a += (self.face_value * self.coupon[i] / 2) * math.e ** (
                    -self.spot_rate[i] * self.time_values[i])
        return a

    def get_spot_values(self):
        """First call above helper function to get rt1, append to the list.
            Then rt1 already computed and added to the list, now substituting to
            formula, getting all remaining spots rate until rt10, and return
            the entire list to plot graph. The entire summation part for the
            i^th term is done by helper function above."""
        self.spot_rate.append(self.get_r_t1())
        for i in range(1, len(self.numbers_of_payments)):
            dirty_price = (0.5 - self.time_to_first_coupon_payment) * \
                          self.coupon[i] * self.face_value + self.price[i]
            self.spot_rate.append(
                -math.log((dirty_price - self.get_the_summation_part())
                          / (self.face_value * self.coupon[i]
                             + self.face_value))
                / (self.time_values[-1] + 0.5))
            self.time_values.append(self.time_values[-1] + 0.5)
        return self.spot_rate

    def get_time_values(self):
        """x-axis for spot rate plot, to be returned to main script."""
        return self.time_values

    def get_yield_values(self):
        """Append all yield values and return the list, for 5(b)"""
        for i in range(len(self.coupon)):
            self.yield_values.append((self.face_value * self.coupon[i] / 2 +
                                      ((self.face_value - self.price[i]) /
                                       self.numbers_of_payments[i]))
                                     / ((self.face_value + self.price[i]) / 2))

        return self.yield_values

    def get_numbers_of_payments(self):
        """x-axis for yield rate plot, 5(b)"""
        return self.numbers_of_payments

    def get_forward_rates(self):
        """5(c), x-axis is defined in the main script (just 5 years)."""
        for i in range(0, 5):
            self.forward_rates.append(
                ((1 + self.spot_rate[2 * i]) ** (2 * i + 1) /
                 (1 + self.spot_rate[2 * i - 2])) ** (2 * i - 1) - 1)
        return self.forward_rates

