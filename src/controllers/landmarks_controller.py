from src.controllers.ExerciseAnalyzer import ExerciseAnalyzer
from src.controllers.DataProcessor import DataProcessor
from src.models.models import PatientStats, Exercises
from src.extensions import db


def calculate_exercise():
    data_path = '/tmp/landmarks.csv'
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

    if len(series_times) == 0:
        return {
            "total_time": total_time,
            "average_series_time": 0,
            "average_time_between_reps": 0,
            "reps_per_series": 0
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
    self, patient_id, exercise_id, landmarks_formatted, date, fps
):

    """
        Falta recoger los datos del paciente, a través del número de tablet
        que deberá pasar la aplicación móvil, con eso coger el patient_id
        y junto con el resultado de analyze_exercise_data, guardar los
        datos en BBDD.

        Cabría pensar si vale la pena crear otra FK en la tabla de
        patient_stats que sea exercise_id, y tener un
        seguimiento de a que ejercicio se refieren esas estadísticas.
    """

    output_path = r"/tmp/landmarks.csv"

    # Uso de la clase
    processor = DataProcessor(landmarks_formatted, output_path=output_path)
    # landmarks_df = processor.landmarks_df
    processor.save_to_csv()

    data = calculate_exercise()
    # exercise_name = Exercises.query.filter_by(id=exercise_id).first().name
    # data =  calculate_exercise(landmarks_formatted, exercise_name, fps)
    landmarks_data = analyze_exercise_data(data)

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
