import { useEffect, useRef, useState } from "react";


function useArgusEvents() {

    const [events, setEvents] = useState([]);

    const [connected, setConnected] = useState(false);

    const socketRef = useRef(null);

    const mountedRef = useRef(false);


    useEffect(() => {

        mountedRef.current = true;


        // ====================================================
        // CREATE WEBSOCKET
        // ====================================================

        const socket = new WebSocket(
            "ws://127.0.0.1:8000/ws/events"
        );

        socketRef.current = socket;


        // ====================================================
        // OPEN
        // ====================================================

        socket.onopen = () => {

            if (!mountedRef.current) {
                return;
            }

            console.log(
                "Connected to Argus event stream."
            );

            setConnected(true);
        };


        // ====================================================
        // MESSAGE
        // ====================================================

        socket.onmessage = (message) => {

            if (!mountedRef.current) {
                return;
            }

            try {

                const event = JSON.parse(
                    message.data
                );

                console.log(
                    "Argus Event:",
                    event
                );


                setEvents(
                    (previousEvents) => {

                        return [
                            event,
                            ...previousEvents
                        ].slice(0, 50);

                    }
                );

            } catch (error) {

                console.error(
                    "Failed to parse Argus event:",
                    error
                );

            }
        };


        // ====================================================
        // ERROR
        // ====================================================

        socket.onerror = () => {

            /*
             * Browser WebSocket errors do not contain
             * useful details in most cases.
             *
             * Do not treat an error during cleanup as
             * an application failure.
             */

            if (!mountedRef.current) {
                return;
            }

            console.error(
                "Argus WebSocket connection error."
            );
        };


        // ====================================================
        // CLOSE
        // ====================================================

        socket.onclose = (event) => {

            if (!mountedRef.current) {
                return;
            }

            console.log(
                "Disconnected from Argus event stream.",
                {
                    code: event.code,
                    reason: event.reason
                }
            );

            setConnected(false);
        };


        // ====================================================
        // CLEANUP
        // ====================================================

        return () => {

            mountedRef.current = false;

            /*
             * Remove handlers before closing the socket.
             *
             * This prevents the intentional cleanup close
             * from triggering our normal error/close logic.
             */

            socket.onopen = null;
            socket.onmessage = null;
            socket.onerror = null;
            socket.onclose = null;


            if (
                socket.readyState === WebSocket.OPEN ||
                socket.readyState === WebSocket.CONNECTING
            ) {

                socket.close();
            }


            if (
                socketRef.current === socket
            ) {

                socketRef.current = null;
            }

        };

    }, []);


    // ========================================================
    // RETURN
    // ========================================================

    return {
        events,
        connected
    };
}


export default useArgusEvents;