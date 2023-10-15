import { useState, useEffect } from 'react';
import YouTube from 'react-youtube';
import { Button } from 'react-bootstrap';

function YouTubePlayer({ videos, videoWidth, videoHeight }) {
  const [player, setPlayer] = useState(null);
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);

  const onReady = (event) => {
    setPlayer(event.target);
  };

  const playVideo = () => {
    if (player) {
      player.playVideo();
    }
  };

  const pauseVideo = () => {
    if (player) {
      player.pauseVideo();
    }
  };

  useEffect(() => {
    setCurrentVideoIndex(0);
    pauseVideo();
  }, [videos]);

  const handlePreviousVideo = () => {
    if (currentVideoIndex > 0) {
      setCurrentVideoIndex(currentVideoIndex - 1);
      pauseVideo();
    }
  };

  const handleNextVideo = () => {
    if (currentVideoIndex < videos.length - 1) {
      setCurrentVideoIndex(currentVideoIndex + 1);
      pauseVideo();
    }
  };

  return (
    <div>
      <YouTube className='d-flex justify-content-center' videoId={videos[currentVideoIndex]} onReady={onReady} opts={{ width: videoWidth, height: videoHeight }} />
      <div className='d-flex justify-content-between px-4 py-2'>
        <Button variant="primary" onClick={handlePreviousVideo} disabled={currentVideoIndex === 0}>
          Previous
        </Button>
        <Button variant="primary" onClick={handleNextVideo} disabled={currentVideoIndex === videos.length - 1}>
          Next
        </Button>
      </div>
    </div>
  );
}

export default YouTubePlayer;
