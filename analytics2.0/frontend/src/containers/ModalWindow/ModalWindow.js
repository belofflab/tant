import React from 'react';
import { Box, Modal } from '@mui/material';
import ColorButton from '../../components/ColorButton';
const style = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  textAlign: 'center',
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 365,
  bgcolor: 'background.paper',
  // border: '2px solid #000',
  boxShadow: 25,
  p: 2,
  borderRadius: 5
};

const ModalWindow = ({ children, title, open, handleModal }) => {

  return (
    <div>
      <ColorButton scolor="#4caf50" onClick={() => handleModal(true)}>{title}</ColorButton>
      <Modal
        open={open}
        onClose={() => handleModal(false)}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          {children}
        </Box>
      </Modal>
    </div>
  );
}


export default ModalWindow;