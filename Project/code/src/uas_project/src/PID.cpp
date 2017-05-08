/*
*   PID controller
*/

#include "PID.hpp"
#include <iostream>
#include <cassert>
#include  <algorithm>

PID::PID(double kp, double ki, double kd, double dt, double max, double min)
{
    this->_kp = kp;
    this->_ki = ki;
    this->_kd = kd;
    this->_dt = dt;
    this->_max = max;
    this->_min = min;
    this->_integral = 0;
    this->_lastError = 0;

    assert(dt != 0.0);
}

double PID::calculate(double setpoint, double feedback)
{
    double error = setpoint - feedback;

    // Proportional term
    double pOut = this->_kp * error;

    // Integral term
    this->_integral += error * _dt;
    double iOut = this->_ki * this->_integral;

    // Derivative term
    double dOut = this->_kd * (error - this->_lastError)/this->_dt;


    // PID output
    double output = pOut + iOut + dOut;

    // Clamp output to min and max.
    output = std::min(this->_max, output);
    output = std::max(this->_min, output);
    _lastError = error;

    return output;
}
