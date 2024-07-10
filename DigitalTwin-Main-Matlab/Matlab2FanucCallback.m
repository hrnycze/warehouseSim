function [fanuc_state, simOut] = Matlab2FanucCallback()

global konec_time

% Adjust paths according to your setup
python_script_path = "C:\Users\Jan-Lenovo\Documents\HoufekGJ\warehouseSim\Focas-Communication-CNC-Python\Python\Matlab2FocasCallback.py"; % e.g., 'C:\Users\yourname\myscript.py'
python_32_interpreter_path = 'C:\Users\Jan-Lenovo\.conda\envs\py310_32\python.exe';


%% synchronous run

% % Use the system function to run the script
% [status, result] = system(sprintf('"%s" "%s"', python_32_interpreter_path, python_script_path));
% 
% % Display the result
% disp(result);
% 
% % Check for errors
% if status ~= 0
%     error('Failed to run Python script: %s', result);
% end

%% asynchronous run

% Create a function handle to run the Python script
runPythonScript = @() system([sprintf('"%s" "%s"', python_32_interpreter_path, python_script_path)]);

% Use parfeval to run the Python script in a background worker
pool = gcp();  % Get the current parallel pool, or create a new one
f = parfeval(pool, runPythonScript, 1);  % 1 is the number of output arguments

% Continue with other MATLAB operations
disp('Python script is running in the background...');

% You can perform other tasks here
disp('Performing other MATLAB-Simulink-Simscape operations...');

GenerovaniTrajektorie();
simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(konec_time));
pause(konec_time-1.5);


% Wait for the Python script to finish and get the output
result = fetchOutputs(f);
disp('Python script completed.');
disp(result);

fanuc_state = result;

end