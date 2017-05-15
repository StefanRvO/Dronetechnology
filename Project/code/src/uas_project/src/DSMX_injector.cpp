#include "Autonomous-precision-landing_BScF16_MHE-TL/Drone-system/DSM_analyser.hpp"
#include <iostream>
#include <string>
#include <cstdio>
#include <cmath>
#include <thread>
#include <chrono>
#include <mutex>          // std::mutex
#include <ros/ros.h>
#include "geometry_msgs/PointStamped.h"

class DSMX_injector
{
    public:
        DSMX_injector(std::string device, ros::NodeHandle *_nh,
                                            uint8_t overwrite_channel,
                                            uint8_t throttle_channel,
                                            uint8_t yaw_channel,
                                            uint8_t pitch_channel,
                                            uint8_t roll_channel);
        void run_thread();
        void print_all();
        void throttle_callback(const geometry_msgs::PointStamped data);
        void pitch_callback(const geometry_msgs::PointStamped data);
        void yaw_callback(const geometry_msgs::PointStamped data);
        void roll_callback(const geometry_msgs::PointStamped data);
        void change_channel_offset(uint8_t channel, int16_t offset);

    private:

        uint8_t overwrite_channel;
        uint8_t yaw_channel;
        uint8_t pitch_channel;
        uint8_t roll_channel;
        uint8_t throttle_channel;
        DSM_RX_TX dsm_analyser;
        std::thread analyser_thread;
        std::mutex mtx;
        bool stop = false;
        bool overwrite = false;
        ros::NodeHandle *nh;
        ros::Subscriber throttle_sub;
        ros::Subscriber yaw_sub;
        ros::Subscriber pitch_sub;
        ros::Subscriber roll_sub;

};


DSMX_injector::DSMX_injector(std::string device, ros::NodeHandle *_nh,
                                    uint8_t _overwrite_channel,
                                    uint8_t _throttle_channel,
                                    uint8_t _yaw_channel,
                                    uint8_t _pitch_channel,
                                    uint8_t _roll_channel)
:overwrite_channel(_overwrite_channel), yaw_channel(_yaw_channel), pitch_channel(_pitch_channel),
roll_channel(_roll_channel), throttle_channel(_throttle_channel), dsm_analyser((char *)device.c_str()), analyser_thread(&DSMX_injector::run_thread, this),
nh(_nh),
throttle_sub(nh->subscribe<geometry_msgs::PointStamped>("/yaw_offset",5, &DSMX_injector::throttle_callback, this)),
yaw_sub(nh->subscribe<geometry_msgs::PointStamped>("/throttle_offset",5, &DSMX_injector::yaw_callback, this)),
pitch_sub(nh->subscribe<geometry_msgs::PointStamped>("/pitch_offset",5, &DSMX_injector::pitch_callback, this)),
roll_sub(nh->subscribe<geometry_msgs::PointStamped>("/roll_offset",5, &DSMX_injector::roll_callback, this))
{
}

void DSMX_injector::throttle_callback(const geometry_msgs::PointStamped data)
{
    this->change_channel_offset(this->throttle_channel, data.point.x);
}

void DSMX_injector::yaw_callback(const geometry_msgs::PointStamped data)
{
    this->change_channel_offset(this->yaw_channel, data.point.x);
}

void DSMX_injector::roll_callback(const geometry_msgs::PointStamped data)
{
    std::cout << "roll_offset: " << data << std::endl;
    this->change_channel_offset(this->roll_channel, data.point.x);
}

void DSMX_injector::pitch_callback(const geometry_msgs::PointStamped data)
{
    this->change_channel_offset(this->pitch_channel, data.point.x);
}

void DSMX_injector::change_channel_offset(uint8_t channel, int16_t offset)
{
    this->mtx.lock();
    if(this->overwrite)
    {
        this->dsm_analyser.change_channel_offset(channel, offset);
    }
    this->mtx.unlock();
}

void DSMX_injector::run_thread()
{
    while(!this->stop)
    {
        std::cout << "analysing\n" << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        this->mtx.lock();
        this->dsm_analyser.DSM_analyse(false);
        this->overwrite = (dsm_analyser.get_in_channel_value(this->overwrite_channel) < 800);
        if(this->overwrite == false)
        {
            this->dsm_analyser.change_channel_offsets(0,0,0,0,0,0,0);
        }
        this->mtx.unlock();
        //this->print_all();
    }
}


void DSMX_injector::print_all()
{
    printf(
        "\nRX frame\nChannel  Value\n0\t%i\n1\t%i\n2\t%i\n3\t%i\n4\t%i\n5\t%i\n6\t%i\n7\t%i\n",
        this->dsm_analyser.get_in_channel_value(0),
        this->dsm_analyser.get_in_channel_value(1),
        this->dsm_analyser.get_in_channel_value(2),
        this->dsm_analyser.get_in_channel_value(3),
        this->dsm_analyser.get_in_channel_value(4),
        this->dsm_analyser.get_in_channel_value(5),
        this->dsm_analyser.get_in_channel_value(6),
        this->dsm_analyser.get_in_channel_value(7)
    );
}



int main(int argc, char **argv)
{
    std::string port;
    ros::init(argc, argv, "dsmxInjector");
    ros::NodeHandle nh("~");

    nh.param<std::string>("uart_device", port, "/dev/ttyAMA0");
    std::cout << port << std::endl;
    DSMX_injector injector(port, &nh, 4, 0, 1, 2, 3);
    ros::spin();
}
