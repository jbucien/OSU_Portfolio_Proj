import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

export const EditExercisePage = ({exerciseToEdit}) => {
    const history = useHistory();

    const [name, setName] = useState(exerciseToEdit.name);
    const [reps, setReps] = useState(exerciseToEdit.reps);
    const [weight, setWeight] = useState(exerciseToEdit.weight);
    const [unit, setUnit] = useState(exerciseToEdit.unit);
    const [date, setDate] = useState(exerciseToEdit.date);

    const editExercise = async () => {
        const editedExercise = {name, reps, weight, unit, date};
        const response = await fetch(`/exercises/${exerciseToEdit._id}`, {
            method: 'PUT',
            body: JSON.stringify(editedExercise),
            headers: {'Content-Type': 'application/json'}
        });
        if(response.status === 200) {
            alert('Successfully edited exercise entry.')
        } else {
            alert(`Failed to edit exercise entry, status code = ${response.status}`);
        }
        history.push('/');
    };

    return (
        <article class="page-content">
            <h2>Edit Exercise Entry</h2>
            <form>
                <div className="form-entry">
                    <label for="name">Exercise Name: </label>
                    <input
                        id="name"
                        type="text"
                        value={name}
                        onChange={e => setName(e.target.value)}/>            
                </div>
                <div className="form-entry">
                    <label for="reps">Number of Repetitions: </label>
                    <input
                        id="reps"
                        type="number"
                        value={reps}
                        onChange={e => setReps(e.target.value)}/>
                </div>
                <div className="form-entry">
                    <label for="weight">Weight: </label>
                    <input
                        id="weight"
                        type="number"
                        value={weight}
                        onChange={e => setWeight(e.target.value)}/>                
                </div>
                <div className="form-entry">
                    <label for="unit">Unit: </label>
                    <select
                        id="unit" 
                        value={unit} 
                        onChange={e => setUnit(e.target.value)} >
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
                        type="date"
                        value={date}
                        onChange={e => setDate(e.target.value)}/>              
                </div>
            </form>
            <button onClick={editExercise}>Save Changes</button>
        </article>
    );
}

export default EditExercisePage;