import React from 'react';
import { RiDeleteBin6Line } from 'react-icons/ri';
import { RiEdit2Line } from 'react-icons/ri';

function Exercise({exercise, onDelete}) {
    return (
        <tr>
            <td>{exercise.name}</td>
            <td>{exercise.reps}</td>
            <td>{exercise.weight}</td>
            <td>{exercise.unit}</td>
            <td>{exercise.date}</td>
            <td><RiEdit2Line/></td>
            <td><RiDeleteBin6Line onClick={ () => onDelete(exercise._id)}/></td>
        </tr>
    );
}

export default Exercise;