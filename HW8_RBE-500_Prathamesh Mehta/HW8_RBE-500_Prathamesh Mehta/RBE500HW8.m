clc, clear all;

bel_door_open = 0.5;
bel_door_closed = 0.5;

sense_open_isopen = 0.6;
sense_closed_isopen = 0.4;
sense_open_isclosed = 0.2;
sense_closed_isclosed = 0.8;

action_isopen_push_isopen = 1;
action_isclosed_push_isopen = 0;
action_isopen_push_isclosed = 0.8;
action_isclosed_push_isclosed = 0.2;

action_isopen_donothing_isopen = 1;
action_isclosed_donothing_isopen = 0;
action_isopen_donothing_isclosed = 0;
action_isclosed_donothing_isclosed = 1;


action = ["do_nothing", "open", "do_nothing", "open", "do_nothing"];
measurement = ["closed", "closed", "closed", "open", "open"];
s = size(action);

for i = 1:s(2)

 disp("Iteration  "+i);
 
if action(i) == "do_nothing"
    bel_bar_open = ((action_isopen_donothing_isopen*bel_door_open)+ action_isopen_donothing_isclosed*bel_door_closed);
    bel_bar_closed = ((action_isclosed_donothing_isopen*bel_door_open)+ action_isclosed_donothing_isclosed*bel_door_closed);
else
    bel_bar_open = ((action_isopen_push_isopen*bel_door_open)+ action_isopen_push_isclosed*bel_door_closed);
    bel_bar_closed = ((action_isclosed_push_isopen*bel_door_open)+ action_isclosed_push_isclosed*bel_door_closed);
end
if measurement(i) == "open"
    bel_open = sense_open_isopen*bel_bar_open;
    bel_closed = sense_open_isclosed*bel_bar_closed;
else 
    bel_open = sense_closed_isopen*bel_bar_open;
    bel_closed = sense_closed_isclosed*bel_bar_closed;
end

normalizer = 1/(bel_open+bel_closed);

bel_door_open = normalizer*bel_open;
bel_door_closed = normalizer*bel_closed;

disp("The belief when door is open is "+bel_door_open);
disp("The belief when door is closed is "+bel_door_closed);
disp(' ');
end


