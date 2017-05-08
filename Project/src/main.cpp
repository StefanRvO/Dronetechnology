#include "DSM_analyser.hpp"
#include <iostream>
#include <string>
#include <cstdio>
#include <cmath>

#define OVERWRITE_CHANNEL 4


void print_in_frame(DSM_RX_TX &con)
{
  printf(
        "\nRX frame\nChannel  Value\n0\t%i\n1\t%i\n2\t%i\n3\t%i\n4\t%i\n5\t%i\n6\t%i\n7\t%i\n",
        con.get_in_channel_value(0),
        con.get_in_channel_value(1),
        con.get_in_channel_value(2),
        con.get_in_channel_value(3),
        con.get_in_channel_value(4),
        con.get_in_channel_value(5),
        con.get_in_channel_value(6),
        con.get_in_channel_value(7)
    );
}


int main(int argc, char const *argv[]) {
    std::string port(argv[1]);
    DSM_RX_TX dsm_analyser((char *)port.c_str());
    double cnt = 0;
    for(uint64_t i = 0; ; i++)
    {
        //printf("test\n");
        cnt += 0.05;
        dsm_analyser.DSM_analyse(false);
        print_in_frame(dsm_analyser);
        if(dsm_analyser.get_in_channel_value(OVERWRITE_CHANNEL) < 800)
        {
            dsm_analyser.change_channel_offsets(0,0,0,0,0,0,0);
            continue;
        }

        dsm_analyser.change_channel_offset(0, sin(cnt) * 700);
    }
    return 0;
}
