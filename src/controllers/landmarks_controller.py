from src.controllers.ExerciseAnalyzer import ExerciseAnalyzer


def calculate_exercise():
    data_path = './src/assets/data_labeled_15.csv'
    datos = ExerciseAnalyzer(data_path, "squat")

    formatted_data = datos.analyze_exercise()
    return formatted_data


def analyze_exercise_data(data):
    total_time = 0
    total_reps = 0
    series_times = []
    reps_per_series = []
    time_between_reps = []

    for series, values in data.items():
        for time_range, reps in values.items():
            start_time, end_time = map(
                float, time_range.strip('()').split(',')
            )
            series_time = end_time - start_time
            total_time += series_time
            series_times.append(series_time)
            reps_per_series.append(len(reps))
            total_reps += len(reps)

            # Calculate time between reps
            if len(reps) > 1:
                for i in range(1, len(reps)):
                    time_between_reps.append(reps[i] - reps[i-1])

    average_series_time = total_time / len(series_times)
    average_time_between_reps = sum(time_between_reps) / len(
        time_between_reps
    ) if time_between_reps else 0

    return {
        "total_time": total_time,
        "average_series_time": average_series_time,
        "average_time_between_reps": average_time_between_reps,
        "reps_per_series": reps_per_series
    }
