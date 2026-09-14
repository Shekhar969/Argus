import cv2


class ZoneSelector:

    def __init__(self, frame):

        self.frame = frame.copy()
        self.display_frame = frame.copy()

        self.points = []

        self.window_name = "Argus - Zone Selector"

    def mouse_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            self.points.append((x, y))

            print(
                f"Point {len(self.points)}: ({x}, {y})"
            )

            self.redraw()

    def redraw(self):

        self.display_frame = self.frame.copy()

        # Draw points
        for index, point in enumerate(self.points):

            cv2.circle(
                self.display_frame,
                point,
                6,
                (0, 0, 255),
                -1
            )

            cv2.putText(
                self.display_frame,
                str(index + 1),
                (point[0] + 10, point[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

        # Draw connecting lines
        if len(self.points) > 1:

            for index in range(
                len(self.points) - 1
            ):

                cv2.line(
                    self.display_frame,
                    self.points[index],
                    self.points[index + 1],
                    (0, 255, 0),
                    2
                )

        # Close polygon preview
        if len(self.points) >= 3:

            cv2.line(
                self.display_frame,
                self.points[-1],
                self.points[0],
                (255, 0, 0),
                2
            )

        # Instructions
        cv2.putText(
            self.display_frame,
            "Click points | ENTER: confirm | R: reset | ESC: cancel",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    def select(self):

        cv2.namedWindow(
            self.window_name
        )

        cv2.setMouseCallback(
            self.window_name,
            self.mouse_callback
        )

        self.redraw()

        while True:

            cv2.imshow(
                self.window_name,
                self.display_frame
            )

            key = cv2.waitKey(20) & 0xFF

            # ENTER → confirm
            if key == 13:

                if len(self.points) < 3:

                    print(
                        "A zone requires at least 3 points."
                    )

                    continue

                print("\nZone confirmed.")

                break

            # R → reset
            elif key == ord("r"):

                self.points = []

                print(
                    "Zone reset."
                )

                self.redraw()

            # ESC → cancel
            elif key == 27:

                self.points = []

                print(
                    "Zone selection cancelled."
                )

                break

        cv2.destroyWindow(
            self.window_name
        )

        return self.points