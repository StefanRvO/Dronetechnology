#ifndef _PID_H_
#define _PID_H_
#include <iostream>
#include "std_msgs/Int16.h"

using namespace std;

class PID
{
    public:
        PID(double kp, double ki, double kd, double dt, double max, double min);
        double calculate(double setpoint, double feedback);
    private:
        double _kp;
        double _ki;
        double _kd;
        double _dt;
        double _max;
        double _min;
        double _integral;
        double _lastError;
};

#endif
