from src.controllers.ExerciseAnalyzerv2 import ExerciseAnalyzerv2
from src.controllers.DataProcessorv2 import DataProcessorv2
from src.models.models import PatientStats, Exercises
from src.extensions import db


def calculate_exercise(exercise_name):
    data_path = '/tmp/landmarks.csv'
    datos = []
    datos = ExerciseAnalyzerv2(data_path, exercise_name)

    formatted_data = []
    formatted_data = datos.analyze_exercise()
    datos.create_graph()
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

    if len(series_times) == 0:
        return {
            "total_time": total_time,
            "average_series_time": 0,
            "average_time_between_reps": 0,
            "reps_per_series": reps_per_series
        }

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


def ProcessLandmarks(
    self, patient_id, exercise_name, landmarks_formatted, date, fps
):
    data = {}
    processor = {}

    output_path = r"/tmp/landmarks.csv"

    # Uso de la clase
    processor = DataProcessorv2(landmarks_formatted, output_path=output_path)
    # landmarks_df = processor.landmarks_df
    processor.save_to_csv()

    data = calculate_exercise(exercise_name)
    print(f"INFORMACIÓN SALIDA DEL MÓDULO IA: {data}")
    print(f"Nombre del ejercicio: {exercise_name}")
    exercise = Exercises.query.filter_by(name=exercise_name).first()

    print(exercise)

    exercise_id = exercise.id
    # data =  calculate_exercise(landmarks_formatted, exercise_name, fps)
    landmarks_data = analyze_exercise_data(data)
    print(f"INFORMACIÓN SALIDA DEL FORMATEADOR: {landmarks_data}")

    patient_stats = PatientStats(
        patient_id=patient_id,
        total_time=landmarks_data["total_time"],
        average_series_time=landmarks_data["average_series_time"],
        average_time_between_reps=landmarks_data["average_time_between_reps"],
        reps_per_series=landmarks_data["reps_per_series"],
        exercise_id=exercise_id
    )

    db.session.add(patient_stats)
    db.session.commit()

    return {"message": "Landmarks processed successfully"}, 201
