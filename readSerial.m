s = serial('COM7', 'BaudRate', 9600);
s.InputBufferSize = 60;
disp(s);
% A = zeros(6,1);
% temp = zeros(6,1)-1;

fopen(s);
fwrite(s,1);
pause(20);
% while 1
%     if s.BytesAvailable == 6
%         temp = fread(s);
%     end
%     if temp(1) == 255
%         break
%     elseif temp(1) == -1
%         continue
%     else
%         A = [A;temp];
%     end
% end
disp(s);
fclose(s);
disp('done');