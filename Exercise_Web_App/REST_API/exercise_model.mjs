// Get the mongoose object
import { query } from 'express';
import mongoose from 'mongoose';
import { password } from './password.mjs';


// Prepare the database "exercises" in the MongoDB Cloud server
mongoose.connect(password,
    {useNewUrlParser: true}
);

//Connect to the database
const db = mongoose.connection;
// The open event is called when the database connection successfully opens
db.once("open", () => {
    console.log("Successfully connected to MongoDB using Mongoose!")
});

//Define the schema
const exerciseSchema = mongoose.Schema({
    name: {type: String, required: true},
    reps: {type: Number, required: true, min: 0},
    weight: {type: Number, required: true, min: 0},
    unit: {type: String, required: true},  // "kgs" or "lbs"
    date: {type: String, required: true} // "MM-DD-YY"
});

/**
 * Compile the model from the schema. 
 */
const Exercise = mongoose.model("Exercise", exerciseSchema);

/** CREATE - an exercise entry
 * @param {String} name
 * @param {Number} reps
 * @param {Number} weight
 * @param {String} unit
 * @param {String} date
 * @returns A promise. Resolves to the JSON object for the document created by calling save
 */
 const createExercise = async (name, reps, weight, unit, date) => {
    // Call the constructor to create an instance of the model class Movie
    const exercise = new Exercise({name: name, reps: reps, weight: weight, unit: unit, date: date });
    // Call save to persist this object as a document in MongoDB
    return exercise.save();
}


/** RETRIEVE - Retrieve a JSON array containing the entire collection
 * @params none 
 * @returns the result of a query object
 */
const retrieveExercises = async () => {
    const query = Exercise.find({});        // filter is an empty object 
    return query.exec();
}

/**UPDATE - replaces an exercise entry with the matching _id with the input properties 
 * @param {String} _id
 * @param {String} name
 * @param {Number} reps
 * @param {Number} weight
 * @param {String} unit
 * @param {String} date
 * @returns a promise. Resolves to the number of documents modified
 */
const updateExercise = async(_id, name, reps, weight, unit, date) => {
    const queryParams = [name, reps, weight, unit, date];
    if(queryParams.includes("") || queryParams.includes(null)) {
        throw err;
    } else {
        const result = await Exercise.replaceOne({_id: _id}, {name: name, reps: reps, weight: weight, unit: unit, date: date });
        return result.modifiedCount;
    };
};

/**DELETE - Deletes a exercise entry with the matching _id
 * @param {String} _id
 * @returns A promise. Resolves to the number of documents deleted.
  */
const deleteExercise = async (_id) => {
    const result = await Exercise.deleteOne({_id: _id});
    return result.deletedCount;
}
// export methods
export {createExercise, retrieveExercises, updateExercise, deleteExercise};
