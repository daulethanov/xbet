import React from "react";
import './cardOpenMatches.css';

function CardOpenMatches({name, start_math}) {
    const formattedStartMath = start_math.replace("T", " ");

    return (
        <div style={{ width: '287px', height: '170px', borderRadius: '10px', overflow: 'hidden' }}>
            <div className="card__open__matches">
                <div className="card__open__matches__block">
                    <h2>{name}</h2>
                    <div style={{width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-evenly'}}>
                        <img src="img/foto.jpg" alt="" />
                        <div style={{textAlign: 'left'}}>
                            <h4>{formattedStartMath}</h4>
                         
                        </div>
                    </div>
                    <h3>Организатор: Анатолий Георгеевич</h3>
                </div>
            </div>
        </div>
    )
}

export default CardOpenMatches;