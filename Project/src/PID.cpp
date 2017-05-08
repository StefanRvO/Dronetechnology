/*
*   PID controller 
*/

#include "PID.hpp"

PID::PID(double kp, double ki, double kd, double dt, double max, double min)
{
    _kp = kp;
    _ki = ki;
    _kd = kd;
    _dt = dt;
    _max = max;
    _min = min;
    _integral = 0;
    _lastError = 0;

    if(dt == 0.0)
        cout << "ERROR: dt cannot be zero!" << endl;
}

double PID::calculate(double setpoint, double feedback)
{
    double error = setpoint - feedback;

    // Proportional term
    double pOut = _kp * error;

    // Integral term
    _integral += error * _dt;
    double iOut = _ki * _integral;

    // Derivative term
    double dOut = _kd * (error - _lastError)/_dt;


    // PID output
    double output = pOut + iOut + dOut;

    // Clamp output to min and max.
    if(output > _max)
        output = _max;
    if(output < _min)
        output = _min;

    _lastError = error;

    return output;
}
