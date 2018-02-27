from numpy.testing import assert_equal, assert_almost_equal
from functions.realised_returns import *
import pytest


@pytest.fixture
def init_params():
    omega = 0
    P = 20
    Q = 300
    V = P * Q
    P_tau = P
    rho = 0.004
    m = 1
    return omega, P, V, Q, P_tau, rho, m

def test_realised_returns_domestic(init_params):
    # if default prob = 0, maturity = 1, P_tau = P, and face_value = P*Q, return is interest rate & m = 1
    omega, P, V, Q, P_tau, rho, m = init_params
    assert_almost_equal(realised_returns(omega, V, P, P_tau, Q, rho, m), rho, 4)

#test_realised_returns_domestic()

def test_realised_returns_foreign(init_params):
    omega, P, V, Q, P_tau, rho, m = init_params
    # with an exchange rate of 1 this should be equal to the previous test
    assert_almost_equal(realised_returns(omega, V, P, P_tau, Q, rho, m, X=1), rho, 4)
