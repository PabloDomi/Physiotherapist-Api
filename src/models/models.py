from src.extensions import db
from sqlalchemy import event


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_token = db.Column(db.String(250), nullable=False)


class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'))


class Routines(db.Model):
    __tablename__ = 'routines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    estimatedTime = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    exercises = db.relationship(
        'Exercises', secondary='routine_exercise', back_populates='routine'
        )


class Exercises(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    routine_ids = db.Column(db.ARRAY(db.Integer))

    routine = db.relationship(
        'Routines', secondary='routine_exercise', back_populates='exercises'
        )


class RoutineExercise(db.Model):
    __tablename__ = 'routine_exercise'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    routine_id = db.Column(
        db.Integer, db.ForeignKey('routines.id'), primary_key=True
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey('exercises.id'), primary_key=True
    )


@event.listens_for(Exercises, 'after_insert')
@event.listens_for(Exercises, 'after_update')
def update_routine_exercise(mapper, connection, target):
    # Verifica si routine_ids está presente en el objeto Exercises
    if hasattr(target, 'routine_ids') and target.routine_ids:
        # Obtiene los IDs de las rutinas ya asociadas a este ejercicio
        existing_routine_ids = connection.execute(
            RoutineExercise.__table__.select().where(
                RoutineExercise.exercise_id == target.id
            )
        ).fetchall()
        # Crea un conjunto de IDs para facilitar la búsqueda
        existing_routine_ids = {
            row['routine_id'] for row in existing_routine_ids
        }
        # Itera sobre los IDs en routine_ids
        for routine_id in target.routine_ids:
            # Comprueba si el ID ya está asociado a este ejercicio
            if routine_id not in existing_routine_ids:
                # Si no está asociado, crea una nueva fila en RoutineExercise
                connection.execute(RoutineExercise.__table__.insert().values(
                    routine_id=routine_id,
                    exercise_id=target.id
                ))
                # Agrega el ID a la lista de IDs asociados
                # para evitar duplicados
                existing_routine_ids.add(routine_id)
