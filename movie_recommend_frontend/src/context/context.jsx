import React, { useState, useContext, createContext } from "react";

const RatingContext = createContext(null);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////

//
// 
export const RatingContextProvider = ({ children }) => {
  const [rating, setRating] = useState([]);
  return (
    // value
    // 평점 조회
    <RatingContext.Provider value={{ rating, setRating }}>
      {children}
    </RatingContext.Provider>
  );
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const useRating = () => {
  const rating = useContext(RatingContext);
  return rating;
};

export const useSetRating = () => {
  const { setRating } = useContext(RatingContext);
  return setRating;
};