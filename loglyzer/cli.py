from loglyzer import __app_name__, __version__
from typing import Optional

import typer
import os
import re
from datetime import datetime
import json

app = typer.Typer()

def version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} v{__version__}')
        raise typer.Exit()

@app.command()
def main(
    path: str = typer.Argument(None, help='Squid Proxy access log file.'),
    version: Optional[bool] = typer.Option(None, '--version', '-v', help='Version information.', callback=version_callback, is_eager=True ),
    most_frequent_ip: Optional[bool] = typer.Option(False, '--mfip', help='Most frequent IP.'),
    least_frequent_ip: Optional[bool] = typer.Option(False, '--lfip', help='Least frequent IP.'),
    events_per_second: Optional[bool] = typer.Option(False, '--eps', help='Events per second.'),
    exchanged_bytes: Optional[bool] = typer.Option(False, '--bytes', help='Total amount of bytes exchanged.')
) -> None:

    if path is None:
        print('No file was specified. Try using --help.')
        raise typer.Exit()

    # Create a list of file paths with provided file path / directory path
    files = []

    if os.path.isdir(path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                files.append(file_path)

    elif os.path.isfile(path):
        files.append(path)
    else:
        print('File type not supported...')

    results = []
    for file_path in files:
        try:
            result = analyze(file_path, most_frequent_ip=most_frequent_ip, least_frequent_ip=least_frequent_ip, events_per_second=events_per_second, exchanged_bytes=exchanged_bytes)
            print(f'[INFO] Analysis results for file {file_path}')
            print(f'[RESULT] {result}')
            results.append({
                'file_path': file_path,
                'analysis_results': result
            })
        except:
            print(f'[ERROR] Could not read file {file_path}')
    
    timestamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

    with open(f'output_{timestamp}.json', 'w') as outfile:
        print(f'[INFO] Results saved to {outfile.name}')
        json.dump(results, outfile)

    return

def analyze(logfile_path: str, most_frequent_ip: bool = False, least_frequent_ip: bool = False, events_per_second: bool = False, exchanged_bytes: bool = False) -> dict:
    """
    This function takes a Squid Proxy acces log file and analyzes its contents

    :most_frequent_ip: identify the most frequent IP/s and its occurrences
    :least_frequent_ip: identify the least frequent IP/s and its occurrences
    :events_per_second: calculate events per second
    :exchanged_bytes: calculate total exchanged bytes

    :return: object with the results
    """ 
    previous_datetime = most_frequent_ips = most_frequent_ips_occurrences = least_frequent_ips = least_frequent_ips_occurrences = None
    total_bytes = total_events = total_seconds = eps = bytes = 0
    ip_occurrences = {}
    output = {}

    with open(logfile_path, mode='r', encoding='utf-8') as file:
            
            for f_line in file:
                line = f_line.rstrip()

                if line:
                    # Log file pattern
                    pattern = re.compile(r'^(\d{10}.\d{3})\s+(\d+)\s(\S+)\s(\S+)\s(\d+)\s(\S+)\s(\S+)\s(\S+)\s(\S+)\s(\S+)')
                    result = pattern.match(line)
                    
                    # If matched result
                    if result:
                        if events_per_second:
                            # Increase event count
                            total_events += 1

                            # Calculate total seconds
                            event_datetime = datetime.fromtimestamp(float(result.group(1)))
                            
                            if previous_datetime is None:
                                previous_datetime = event_datetime
                            
                            if (event_datetime - previous_datetime).total_seconds() > 1:
                                total_seconds += 1
                                previous_datetime = event_datetime

                        if most_frequent_ip or least_frequent_ip:
                            # Increase IP ocurrence count
                            if result.group(3) in ip_occurrences:
                                ip_occurrences[str(result.group(3))] += 1
                            else:
                                ip_occurrences[str(result.group(3))] = 1

                        if exchanged_bytes:
                            # Add exchanged bytes
                            total_bytes += int(result.group(2)) + int(result.group(5))

            if most_frequent_ip:            
                most_frequent_ips = [key for key, value in ip_occurrences.items() if value == max(ip_occurrences.values())]
                most_frequent_ips_occurrences = ip_occurrences[most_frequent_ips[0]]
            
            if least_frequent_ip:
                least_frequent_ips = [key for key, value in ip_occurrences.items() if value == min(ip_occurrences.values())]
                least_frequent_ips_occurrences = ip_occurrences[least_frequent_ips[0]]

            if events_per_second:
                eps = round(total_events / total_seconds, 2)
            
            if exchanged_bytes:
                bytes = round(total_bytes, 0) 
    
    if most_frequent_ip:
        output['most_frequent_ips'] = {
            'list': most_frequent_ips, 
            'occurrences': most_frequent_ips_occurrences
        }
    
    if least_frequent_ip:
        output['least_frequent'] = {
            'list': least_frequent_ips,
            'occurrences': least_frequent_ips_occurrences
        }

    if events_per_second:
        output['events_per_second'] = eps

    if exchanged_bytes:
        output['exchanged_bytes'] = bytes

    return output