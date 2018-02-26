from numpy.testing import assert_equal, assert_almost_equal
from functions.realised_returns import *
import pytest


def test_realised_returns_domestic():
    # if default prob = 0, maturity = 1, P_tau = P, and face_value = P*Q, return is interest rate & m = 1
    omega = 0
    P = 20
    Q = 300
    V = P * Q
    P_tau = P
    rho = 0.004
    m = 1
    assert_almost_equal(realised_returns_domestic(omega, V, P, P_tau, Q, rho, m), rho, 4)

#test_realised_returns_domestic()