import React, { useState } from 'react';
import PropTypes from 'prop-types';
import {
    Box, Typography, Button,
    Rating, Tabs, Tab, styled
} from '@mui/material';
import Review from '../../components/Review';
import MasterWork from '../../components/MasterWork';
import MasterBio from '../../components/MasterBio/MasterBio';

import AddReviewModal from '../../components/AddReviewModal';

function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <Typography
            component="div"
            role="tabpanel"
            hidden={value !== index}
            id={`scrollable-auto-tabpanel-${index}`}
            aria-labelledby={`scrollable-auto-tab-${index}`}
            {...other}
        >
            <Box>{children}</Box>
        </Typography>
    );
}

TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired
};


function a11yProps(index) {
    return {
        id: `scrollable-auto-tab-${index}`,
        "aria-controls": `scrollable-auto-tabpanel-${index}`
    };
}

const ColorButton = styled(Button)(({ scolor }) => ({
    color: "#fff",
    backgroundColor: scolor,
    '&:hover': {
        backgroundColor: scolor,
    },
}));

export default function ProfileDetail({ masterInfo, client, authenticated }) {
    const [value, setValue] = useState(1);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };
    return (
        <Box>
            <Box sx={{
                textAlign: 'center',
                marginTop: 4,
                padding: 3,
                boxShadow: 2,
                borderRadius: 1
            }}>
                <Box
                    component="img"
                    sx={{
                        borderRadius: 5,
                        maxWidth: 150
                    }}
                    alt={masterInfo.profile.full_name}
                    src={process.env.REACT_APP_BACKEND_BASE_URL + masterInfo.profile.avatar?.path}
                />
                <Box>
                    <Typography sx={{ marginTop: 1 }} variant="h5">{masterInfo.profile.full_name} </Typography>
                    <Rating name="half-rating-read" defaultValue={0} value={masterInfo.average_rating} readOnly />
                </Box>
                <Box component="div" sx={{ display: 'flex', justifyContent: 'space-around', marginTop: 2 }}>
                    <ColorButton
                        component="a"
                        target='blank'
                        variant="contained"
                        scolor="#c764d0"
                        href="https://t.me/belofflab"
                    >
                        Записаться
                    </ColorButton>
                    <AddReviewModal mid={masterInfo.id} uid={client} authenticated={authenticated} />
                </Box>
                <Box sx={{ width: '100%', marginTop: 2 }}>
                    <Tabs
                        value={value}
                        onChange={handleChange}
                        textColor="secondary"
                        indicatorColor="secondary"
                        aria-label="secondary tabs example"
                        centered
                    >
                        <Tab label="Био" {...a11yProps(0)} />
                        <Tab label="Отзывы" {...a11yProps(1)} />
                        <Tab label="Работы" {...a11yProps(2)} />
                    </Tabs>
                </Box>
            </Box>
            <TabPanel value={value} index={0}>
                <MasterBio bio={masterInfo.biography} />
            </TabPanel>
            <TabPanel value={value} index={1}>
                <Review masterId={masterInfo.id} />
            </TabPanel>
            <TabPanel value={value} index={2}>
                <MasterWork masterId={masterInfo.id} />
            </TabPanel>
        </Box>
    )
}