import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';


export const CreateExercisePage = () => {
    const history = useHistory();

    const [name, setName] = useState('');
    const [reps, setReps] = useState('');
    const [weight, setWeight] = useState('');
    const [unit, setUnit] = useState('');
    const [date, setDate] = useState('');

    const createExercise = async () => {
        const newExercise = {name, reps, weight, unit, date};
        const response = await fetch('/exercises', {
            method: 'POST',
            body: JSON.stringify(newExercise),
            headers: {'Content-Type': 'application/json'}
        });
        if(response.status === 201) {
            alert('Successfully created a new exercise entry.')
        } else {
            alert(`Failed to create a new exercise entry, status code = ${response.status}`);
        }
        history.push('/');
    };

    return (
        <article class="page-content">
            <h2>Create a New Exercise Entry</h2>
            <input
                type="text"
                placeholder="Name of Exercise"
                value={name}
                onChange={e => setName(e.target.value)} />
            <input
                type="number"
                placeholder="Repetitions"
                value={reps}
                onChange={e => setReps(e.target.value)} />
            <input
                type="number"
                placeholder="Weight"
                value={weight}
                onChange={e => setWeight(e.target.value)} />
            <select 
                value={unit} 
                onChange={e => setUnit(e.target.value)} >
                    <option disabled selected hidden value="">
                        Unit of Measurement</option>
                    <option value="lbs">
                        lbs</option>
                    <option value="kg">
                        kg</option>
            </select>
            <input
                type="text"
                placeholder="MM-DD-YY"
                value={date}
                onChange={e => setDate(e.target.value)} />
            <button onClick={createExercise}>Create</button>
        </article>
    );
}

export default CreateExercisePage;