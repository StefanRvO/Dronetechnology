#include <PID.hpp>
#include <ros/ros.h>
#include "geometry_msgs/PointStamped.h"

class Controller
{
    public:
        Controller(ros::NodeHandle *_nh, float _setpoint_x, float _setpoint_y);
        void pos_callback(geometry_msgs::PointStamped point);
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

void Controller::pos_callback(geometry_msgs::PointStamped point)
{
    //std::cout << point << std::endl;
    geometry_msgs::PointStamped pitch;
    geometry_msgs::PointStamped roll;
    //std::cout << point.x << " " << point.y << std::endl;
    if(point.point.x == -320 && point.point.y == -240)
    {
        pitch.point.x = 0;
        roll.point.x = 0;
    }
    else
    {
        roll.point.x = roll_pid.calculate(this->setpoint_x, point.point.x);
        pitch.point.x = pitch_pid.calculate(this->setpoint_y, point.point.y);
        if( abs(point.point.x) < 50) roll.point.x = 0;
        if( abs(point.point.y) < 50) pitch.point.x = 0;
    }
    pitch.header.stamp = point.header.stamp;
    roll.header.stamp = point.header.stamp;

    this->roll_publisher.publish(roll);
    this->pitch_publisher.publish(pitch);

}


Controller::Controller(ros::NodeHandle *_nh, float _setpoint_x, float _setpoint_y)
: setpoint_x(_setpoint_x), setpoint_y(_setpoint_y),
nh(_nh),
pos_subscriber(this->nh->subscribe<geometry_msgs::PointStamped>("/ball_pos", 1, &Controller::pos_callback, this)),
roll_publisher(this->nh->advertise<geometry_msgs::PointStamped>("/roll_offset",1)),
pitch_publisher(this->nh->advertise<geometry_msgs::PointStamped>("/pitch_offset",1)),
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
