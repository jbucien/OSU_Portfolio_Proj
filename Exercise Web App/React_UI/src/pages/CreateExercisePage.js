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
            <form>
                <div className="form-entry">
                    <label for="name">Exercise Name: </label>
                    <input
                        id="name"
                        type="text"
                        placeholder="Exercise"
                        value={name}
                        onChange={e => setName(e.target.value)} />            
                </div>
                <div className="form-entry">
                    <label for="reps">Number of Repetitions: </label>
                    <input
                        id="reps"
                        type="number"
                        placeholder="0"
                        value={reps}
                        onChange={e => setReps(e.target.value)} />
                </div>
                <div className="form-entry">
                    <label for="weight">Weight: </label>
                    <input
                        id="weight"
                        type="number"
                        placeholder="0"
                        value={weight}
                        onChange={e => setWeight(e.target.value)} />                
                </div>
                <div className="form-entry">
                    <label for="unit">Unit: </label>
                    <select
                        id="unit" 
                        value={unit} 
                        onChange={e => setUnit(e.target.value)} >
                            <option value="" hidden disabled> Weight </option>
                            <option value="lbs">
                                lbs</option>
                            <option value="kgs">
                                kgs</option>
                    </select>               
                </div>
                <div className="form-entry">
                    <label for="date">Date: </label>
                    <input
                        id="date"
                        type="text"
                        placeholder="MM-DD-YY"
                        value={date}
                        onChange={e => setDate(e.target.value)} />              
                </div>
            </form>
            <button onClick={createExercise}>Create</button>
        </article>
    );
}

export default CreateExercisePage;