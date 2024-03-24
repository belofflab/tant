import React from 'react';

import {Button, styled} from '@mui/material';


export const ColorButton = styled(Button)(({ scolor }) => ({
    color: "#fff",
    backgroundColor: scolor,
    '&:hover': {
        backgroundColor: scolor,
    },
  }));