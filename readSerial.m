function res = readSerial()    
    s = serial('COM7', 'BaudRate', 9600);
    disp(s);

    finishup = onCleanup(@() cleanup(ser));           % removes remaining data from the serial reader                                                                                            
        function cleanup(s)
            fclose(s);                                % close the serial reader
            delete(s);                                % delete all information stored in the serial
            clear s                                   % remove data from MATLAB
            disp('Clean!')                            % tells you it cleaned: if it doesn't unplug and replug arduino
        end

    fopen(s);
    pause(5);
    fwrite(s,1);
    pause(20);
    res = fread(s);
    disp(s);
    fclose(s);
    disp('done');
end