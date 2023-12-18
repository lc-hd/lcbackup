import os.path
import sys
import time
from typing import List
from pathlib import Path
from datetime import datetime, timedelta
from collections import namedtuple

import boto3


TIME_FORMAT = '%Y:%m:%d:%H:%M:%S'
Interval = namedtuple('Interval', ['name', 'max_backups'])
INTERVALS = [
    Interval('day', 7),
    Interval('week', 5),
    Interval('month', 12),
    Interval('year', 4),
]
DEBUG = os.environ.get('DEBUG_VALUE')
BOTO_SESSION = boto3.session.Session()
ACCESS_KEY = os.environ.get('DBBACKUP_ACCESS_KEY')
SECRET_KEY = os.environ.get('DBBACKUP_SECRET_KEY')
BUCKET_NAME = os.environ.get('DBBACKUP_BUCKET_NAME')
ENDPOINT_URL = os.environ.get('DBBACKUP_ENDPOINT_URL')


class Storage:
    def __init__(self):

        if not (ACCESS_KEY and SECRET_KEY and BUCKET_NAME and ENDPOINT_URL):
            # raise error if any s3-related env is None
            raise Exception('S3 Bucket Is Not Configured')

        self.client = BOTO_SESSION.client(
            's3',
            region_name='nyc3',
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        a=1


    def write_file(self, file_path: str):
        pass

    def delete_file(self, oldest_file_path: str):
        pass

    def list_directory(self, path: str) -> list:
        return []


class BaseCommand:
    @staticmethod
    def print_error(message: str):
        print(message, file=sys.stderr)

    @staticmethod
    def print_info(message: str):
        print(message, file=sys.stdout)


class Command(BaseCommand):
    help = "Runs backup code"
    storage = Storage()
    env = 'dev' if DEBUG else 'prod'

    @staticmethod
    def truncate_datetime(dt: datetime, interval_name: str) -> datetime:
        """
        Rounds datetime precision down to the nearest year, month, week, or day.
        """

        if interval_name == 'year':
            return datetime(year=dt.year, month=1, day=1)

        elif interval_name == 'month':
            return datetime(year=dt.year, month=dt.month, day=1)

        elif interval_name == 'week':
            # note start of week may be in previous month
            days_after_start_of_week = dt.weekday()
            return datetime(year=dt.year, month=dt.month, day=dt.day) - timedelta(days_after_start_of_week)

        elif interval_name == 'day':
            return datetime(year=dt.year, month=dt.month, day=dt.day)

        else:
            raise Exception('Invalid Interval Name')

    def create_backup(self, file_path: str) -> bool:
        # returns True when backup was created and False otherwise
        try:
            # create backup here
            # management.call_command(dbbackup.Command(), verbosity=0, output_filename=file_path)
            self.storage.write_file(file_path)
            return True
        except (Exception,):
            self.print_error(f'Error Creating File {file_path}')
            return False

    def should_save_new_file(self, interval: Interval, files: List[str]) -> bool:
        if len(files) == 0:
            return True

        most_recent_file_name = Path(files[-1]).stem
        most_recent_file_datetime = datetime.strptime(most_recent_file_name, TIME_FORMAT)

        truncated_recent_file_time = self.truncate_datetime(most_recent_file_datetime, interval.name)
        truncated_current_time = self.truncate_datetime(datetime.now(), interval.name)

        # compare the truncated times to see if they are the same
        return truncated_recent_file_time != truncated_current_time

    def remove_oldest_file(self, interval: Interval, files_in_folder):

        # when folder is empty, skip removing the oldest file
        if len(files_in_folder) == 0:
            return

        # when the file count hasn't reached the limit, skip removing the oldest file
        if len(files_in_folder) <= interval.max_backups:
            return

        oldest_file_name = files_in_folder[0]
        oldest_file_path = os.path.join(self.env, interval.name, oldest_file_name)
        try:
            self.storage.delete_file(oldest_file_path)
            self.print_info(f'Deleted Old Backup For {interval.name} Named {oldest_file_name}')
        except (Exception,):
            self.print_error(f'Error Deleting File {oldest_file_name}')

    def job(self):
        for interval in INTERVALS:
            try:
                path = os.path.join(self.env, interval.name)
                files: list = self.storage.list_directory(path=path)
                files.sort()
            except (Exception,):
                self.print_error('Error Getting Files')
                files = []

            if self.should_save_new_file(interval, files):
                file_name = f'{time.strftime(TIME_FORMAT)}.psql'
                file_path = os.path.join(self.env, interval.name, file_name)
                self.print_info(f'Creating Backup For {interval.name} Named {file_name}')
                creation_successful = self.create_backup(file_path)

                if creation_successful:
                    files.append(file_name)
                    self.remove_oldest_file(interval, files)

        self.print_info('Backup Script Complete')

    def run(self):
        self.print_info('Running backup Script')
        self.job()


if __name__ == "__main__":
    c = Command()
    c.run()
