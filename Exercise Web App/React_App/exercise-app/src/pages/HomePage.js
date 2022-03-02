import ExerciseList from '../components/ExerciseList';
import { useState, useEffect } from 'react';
import { useHistory, Link } from 'react-router-dom';

function HomePage({setExerciseToEdit}) {

    const [exercises, setExercises] = useState([]);
    const history = useHistory()

    const onDelete = async _id => {
        const response = await fetch(`/exercises/${_id}`, {method: 'DELETE'});
        // Need to make sure deletion is successful
        if(response.status === 204){
            // create an updated array of exercise objects and re-render
            setExercises(exercises.filter(e => e._id !== _id))
        } else {
            console.error(`Failed to delete exercise with _id = ${_id}, status code = ${response.status}`);
        }
    };

    const onEdit = exercise => {
        // because we lifted up the state to a common ancestory (App.js), now we can use the variable exercise on the EditExercisePage
        setExerciseToEdit(exercise);
        history.push('/edit-exercise');
    }

    const loadExercises = async () => {
        // fetch returns a promise that resolves to a response object if successful (if the request receives a response)
        // this response obj is part of the browser API, not part of Express
        const response = await fetch('/exercises');
        // response.json() also returns a promise
        const exerciseData = await response.json();
        // useState is updated
        setExercises(exerciseData);
    }
    
    // Note: useEffect() cannot directly take an async function as a param, so it calls an anon funciton which in turn calls loadExercises()
    // Render during mounting stage of component
    useEffect(() => {
        loadExercises();
    }, []);

    return (
        <article class="page-content">
            <h2>List of Exercises</h2>
                <ExerciseList exercises={exercises} onDelete={onDelete} onEdit={onEdit}></ExerciseList>
        </article>
    );
}

export default HomePage;