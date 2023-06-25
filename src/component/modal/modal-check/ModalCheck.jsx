import React from "react";
import './modalCheck.css';

function ModalCheck({modalCheckOpen, setModalCheckOpen}) {

	return (
		<div className={modalCheckOpen ? "modal__check active" : "modal__check"}>
			<div className="modal__check__content">
				<div style={{ display: 'flex', alignItems: 'center', height: '48px', margin: '24px 0 0 24px', gap: '15px' }}>
					<img src="img/foto12.svg" alt="" />
					<div><h3>Счёт матча</h3>
						<h4>Поставьте счёт</h4>
					</div>
				</div>
				<div className="modal__check__content__line"></div>
				<div style={{display:'flex', justifyContent: 'space-evenly', marginTop: '45px'}}>
					<div className="modal__check__content__item">
						<h3>Команда 1</h3>
						<div style={{ width: '100%', display: 'flex', height: '90px', alignItems: 'center', gap: '16px', marginBottom: '12px' }}>
							<button>-</button>
							<span>0</span>
							<button>+</button>
						</div>
					</div>
					<div className="modal__check__content__item">
						<h3>Команда 2</h3>
						<div style={{ width: '100%', display: 'flex', height: '90px', alignItems: 'center', gap: '16px' }}>
							<button>-</button>
							<span>0</span>
							<button>+</button>
						</div>
					</div>
				</div>
				<div className="modal__check__content__line"></div>
				<div style={{marginTop: '24px', display: 'flex', gap: '15px', justifyContent: 'center'}}>
					<button onClick={() => setModalCheckOpen(false)} className="modal__check__content__close">Отмена</button>
					<button className="modal__check__content__accept">Принять</button>
				</div>
			</div>
		</div>
	)

}

export default ModalCheck;