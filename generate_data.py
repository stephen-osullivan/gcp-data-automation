from faker import Faker

import argparse
import datetime
import json

def generate_fake_data(num_records=100):
    """
    Generates fake data with date, names, emails, and expenditure.

    Args:
    num_records: Number of records to generate.

    Returns:
    A list of dictionaries, each containing the generated data.
    """

    fake = Faker()
    data = []
    for _ in range(num_records):
        data.append({
            "date": fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            "name": fake.name(),
            "email": fake.email(),
            "expenditure": round(fake.random.uniform(0, 1000), 2)  # Expenditure between 0 and 1000
        })
    return data


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate fake data')
    parser.add_argument('--num_records', type=int, default=10, help='Number of records to generate')
    args = parser.parse_args()
    
    # Generate fake data
    fake_data = generate_fake_data(num_records=args.num_records)
    
    # Save data to NEWLINE DELIMETED JSON file
    file_name = f'fake_data_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.ndjson'
    with open(file_name, 'w') as f:
        for record in fake_data:
            f.write(json.dumps(record) + '\n')
