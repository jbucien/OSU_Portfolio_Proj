import React from 'react';
import { RiDeleteBin6Line, RiEdit2Line } from 'react-icons/ri';

function Exercise({exercise, onDelete, onEdit}) {
    return (
        <tr>
            <td>{exercise.name}</td>
            <td>{exercise.reps}</td>
            <td>{exercise.weight}</td>
            <td>{exercise.unit}</td>
            <td>{exercise.date}</td>
            <td>
                <button class ="table-icons">
                <RiEdit2Line onClick={ () => onEdit(exercise)}/>
                </button>
            </td>
            <td>
                <button class ="table-icons">
                    <RiDeleteBin6Line onClick={ () => onDelete(exercise._id)}/>
                </button>
            </td>
        </tr>
    );
}

export default Exercise;