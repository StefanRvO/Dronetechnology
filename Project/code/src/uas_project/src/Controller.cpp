#include <PID.hpp>
#include <ros/ros.h>
#include "std_msgs/Int16.h"
#include "geometry_msgs/Point.h"

class Controller
{
    public:
        Controller(ros::NodeHandle *_nh, float _setpoint_x, float _setpoint_y);
        void pos_callback(geometry_msgs::Point point);
    private:
        float setpoint_x;
        float setpoint_y;
        ros::NodeHandle *nh;
        ros::Subscriber pos_subscriber;
        ros::Publisher roll_publisher;
        ros::Publisher pitch_publisher;
        PID roll_pid;
        PID pitch_pid;
};

void Controller::pos_callback(geometry_msgs::Point point)
{
    //std::cout << point << std::endl;
    std_msgs::Int16 pitch;
    std_msgs::Int16 roll;
    //std::cout << point.x << " " << point.y << std::endl;
    if(point.x == -320 && point.y == -240)
    {
        pitch.data = 0;
        roll.data = 0;
    }
    else
    {
        roll.data = roll_pid.calculate(this->setpoint_x, point.x);
        pitch.data = pitch_pid.calculate(this->setpoint_y, point.y);
        if( abs(point.x) < 50) roll.data = 0;
        if( abs(point.y) < 50) pitch.data = 0;
    }
    this->roll_publisher.publish(roll);
    this->pitch_publisher.publish(pitch);

}


Controller::Controller(ros::NodeHandle *_nh, float _setpoint_x, float _setpoint_y)
: setpoint_x(_setpoint_x), setpoint_y(_setpoint_y),
nh(_nh),
pos_subscriber(this->nh->subscribe<geometry_msgs::Point>("/ball_pos", 1, &Controller::pos_callback, this)),
roll_publisher(this->nh->advertise<std_msgs::Int16>("/roll_offset",1)),
pitch_publisher(this->nh->advertise<std_msgs::Int16>("/pitch_offset",1)),
roll_pid(1, 0., 0.1, 1/25., fabs(1705 - 342) / 2., -fabs(1705 - 342) / 2.),
pitch_pid(1, 0., 0.1, 1/25., fabs(1705 - 342) / 2., -fabs(1705 - 342) / 2.)
{
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "controller");
    ros::NodeHandle nh("~");
    Controller con(&nh, 0, 0);
    ros::spin();
    return 0;
}
