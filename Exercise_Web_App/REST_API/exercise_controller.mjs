import * as exercises from './exercise_model.mjs';
import express from 'express';

const PORT = 3000;

const app = express();

app.use(express.json());

/**CREATE a new exercise entry*/
app.post('/exercises', (req, res) => {
    exercises.createExercise(req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
        .then(exercise => {
            console.log('New exercise created.');
            res.set({'Content-Type': 'application/json'});
            res.status(201).json(exercise);
        })
        .catch(error => {
            console.error(error);
            res.status(500).json({Error: 'Request failed'});
        });
});

/**RETRIEVE - Retrieve a JSON array containing the entire collection */
app.get('/exercises', (req, res) => {
    exercises.retrieveExercises()
        .then(exercises => {
            console.log('Exercise(s) retrieved.')
            res.set({'Content-Type': 'application/json'});
            res.status(200).json(exercises);
        })
        .catch(error => {
            console.error(error);
            res.status(500).json({Error: 'Request failed'});
        });
});

/**UPDATE */
app.put('/exercises/:_id', (req, res) => {
    exercises.updateExercise(req.params._id, req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
    .then(modifiedCount => {
        if (modifiedCount === 1) {
            console.log("Exercise updated.")
            res.set({'Content-Type': 'application/json'});
            res.status(200).json({_id: req.params._id, name: req.body.name, reps: req.body.reps, weight: req.body.weight, unit: req.body.unit, date: req.body.date})
        } else {
            console.log("Exercise not found.")
            res.status(404).json({Error: 'Resource not found'});
        }
    })
    .catch(error => {
        console.error(error);
        res.status(500).json({Error: 'Request failed'});
    });
});

/**DELETE */
app.delete('/exercises/:_id', (req, res) => {
    exercises.deleteExercise(req.params._id)
      .then(deletedCount => {
        if (deletedCount === 1) {
            console.log("Exercise deleted.")
            res.status(204).send()
        } else {
        res.status(404).json({Error: 'Resource not found'});
        };
      })
      .catch(error => {
        console.error(error);
        res.status(500).send({Error: 'Request failed'});
      });
  });

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
})