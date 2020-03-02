import React, {useState} from "react";
import StudentAnswer from './StudentAnswer'
import './AnswersList.css';

export default function AnswersList(props) {
    const answers = props.answers
    return(
        <div className="answer-list">
            {answers.map((answer) => {
                return <StudentAnswer key={answer.id} {...answer} />;
            })}
        </div>
    )
}