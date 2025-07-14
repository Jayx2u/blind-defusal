import Image from "next/image";

export default function Home() {
  return (
    <div className="container mx-auto p-4 sm:p-8 font-mono bg-gray-100 text-gray-800">
      <div className="flex justify-center my-4">
        <Image
            src="/blind-defusal-logo.svg"
            alt="Blind Defusal Logo"
            width={350}
            height={350}
            priority
          />
      </div>
      <header className="text-center my-8">
        <h1 className="text-5xl font-bold text-red-600 tracking-wider">
          BOMB DEFUSAL MANUAL
        </h1>
        <p className="text-lg mt-2">
          For use by trained experts only. Read instructions carefully.
        </p>
        <p className="text-sm text-red-700 font-bold mt-1">
          Failure to comply may result in detonation.
        </p>
      </header>

      <main className="space-y-12">
        {/* Introduction Section */}
        <section id="introduction">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Introduction
          </h2>
          <div className="space-y-4 text-lg">
            <p>
              You are the <span className="font-bold">Expert</span>. Your partner, the{" "}
              <span className="font-bold">Operator</span>, has a device with a
              ticking timer that must be disarmed. The Operator cannot see this
              manual, and you cannot see the device.
            </p>
            <p>
              You must communicate effectively to disarm all modules before the
              timer expires. This manual contains the instructions for each
              type of module and type of identifiable features that may appear on the device.
            </p>
          </div>
        </section>

        {/* On the Subject of the Bomb Section */}
        <section id="on-the-bomb">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            On the Subject of the Bomb
          </h2>
          <div className="space-y-4 text-lg">
            <p>
              A bomb will have one or more modules that must be disarmed. Each module is self-contained and can be disarmed in any order. Instructions for each module are below.
            </p>
            <p>
              Some disarming instructions will require information from the bomb itself, such as the serial number or batteries. This information can be found on the bottom of the bomb casing.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white">
              <h3 className="text-xl font-bold mb-2">Timer and Strikes</h3>
              <ul className="list-disc list-inside space-y-2">
                <li>The bomb has a countdown timer. When it reaches 0:00, it will explode.</li>
                <li>
                  If a mistake is made, the bomb will record a strike and the timer will speed up. A small LED above the timer will light for each strike.
                </li>
                <li>
                  If you receive <span className="font-bold text-red-700">three strikes</span>, the bomb will explode.
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Identification: Serial Number Section */}
        <section id="serial-number">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Identification: Serial Number
          </h2>
          <div className="space-y-4 text-lg">
            <p>
              The bomb&apos;s serial number is crucial for disarming certain modules. It can be found on the side of the bomb casing.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white">
              <h3 className="text-xl font-bold mb-2">Serial Number Format</h3>
              <p>
                The serial number consists of a combination of letters and numbers. For example: <span className="font-bold p-1 bg-gray-200 rounded">SN48K2</span>.
              </p>
              <p className="mt-2">
                Pay close attention to specific digits or letters when requested by a module&apos;s instructions, especially whether a digit is <span className="font-bold">odd or even</span>.
              </p>
            </div>
          </div>
        </section>

        {/* Gyro-Stabilizer Module Section */}
        <section id="gyro">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Needy Module: Gyro-Stabilizer
          </h2>
          <div className="space-y-4">
            <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 p-4" role="alert">
              <p className="font-bold">This is a needy module that requires constant supervision.</p>
              <p>It is sensitive to sudden movement. Any sudden movements or incorrect orientations will result in a strike. The module is disarmed once all other modules are solved.</p>
            </div>
            <p>
              The Operator must keep the device as still as possible. Movement is allowed, however the tolerance of movement is unknown.
            </p>
          </div>
        </section>

         {/* Power Sequencer Module Section */}
        <section id="power-sequencer">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Module: Power Sequencer
          </h2>
          <div className="space-y-4">
            <p>
              This module has one colored LED and four corresponding buttons. The LEDs will flash in a sequence. The start of the sequence is indicated by the LED being white. The Operator must describe the color sequence, and the Expert will provide the correct button press sequence, which may depend on the bomb&apos;s serial number.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white">
              <h3 className="text-xl font-bold mb-2">Conditional Sequences:</h3>
              <p>Find the observed color sequence below and follow the condition to determine which buttons to press.</p>
              <table className="w-full mt-2 text-left border-collapse">
                <thead>
                  <tr>
                    <th className="border-b-2 border-gray-300 p-2">Color Sequence</th>
                    <th className="border-b-2 border-gray-300 p-2">Condition</th>
                    <th className="border-b-2 border-gray-300 p-2">Press Sequence</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-200">
                    <td className="p-2" rowSpan={2}>Red → Blue → Green → Yellow</td>
                    <td className="p-2">If last digit of serial is even...</td>
                    <td className="p-2">Button 1, Button 3</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-2">Otherwise...</td>
                    <td className="p-2">Button 2, Button 4</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-2" rowSpan={2}>Yellow → Red → Blue → Green</td>
                    <td className="p-2">If serial has a vowel...</td>
                    <td className="p-2">Button 4, Button 2, Button 1</td>
                  </tr>
                   <tr className="border-b border-gray-200">
                    <td className="p-2">Otherwise...</td>
                    <td className="p-2">Button 3, Button 1</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-2">Blue → Green → Yellow → Red</td>
                    <td className="p-2">Always...</td>
                    <td className="p-2">Button 2, Button 4</td>
                  </tr>
                   <tr className="border-b border-gray-200">
                    <td className="p-2">Green → Yellow → Red → Blue</td>
                    <td className="p-2">Always...</td>
                    <td className="p-2">All Buttons</td>
                  </tr>
                   <tr>
                    <td className="p-2" rowSpan={2}>Red → Red → Blue → Yellow</td>
                    <td className="p-2">If last digit of serial is odd...</td>
                    <td className="p-2">Button 2, Button 2, Button 3</td>
                  </tr>
                  <tr>
                    <td className="p-2">Otherwise...</td>
                    <td className="p-2">Button 1, Button 4</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Morse Code Module Section */}
        <section id="morse-code">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Module: Morse Code
          </h2>
          <div className="space-y-4">
            <p>
              This module has a flashing LED, a sliding potentiometer, and a transmit button. The LED flashes a single word from the list below in Morse code. The start of the sequence is indicated by the LED being blue. The Operator must interpret the code, and the Expert must provide the correct frequency to set with the potentiometer.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white space-y-6">
              <div>
                <h3 className="text-xl font-bold mb-2">Instructions:</h3>
                <ol className="list-decimal list-inside space-y-1">
                  <li>Operator identifies the word being flashed by the LED using the Morse code chart.</li>
                  <li>Expert finds the word in the frequency table to get the correct frequency.</li>
                  <li>Operator adjusts the sliding potentiometer to the specified frequency.</li>
                  <li>Operator presses the transmit button to disarm the module.</li>
                </ol>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2">Frequency Table:</h3>
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr>
                      <th className="border-b-2 border-gray-300 p-2">Word</th>
                      <th className="border-b-2 border-gray-300 p-2">Frequency</th>
                      <th className="border-b-2 border-gray-300 p-2">Word</th>
                      <th className="border-b-2 border-gray-300 p-2">Frequency</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b border-gray-200"><td className="p-2">shell</td><td className="p-2">3.505 MHz</td><td className="p-2">flick</td><td className="p-2">3.555 MHz</td></tr>
                    <tr className="border-b border-gray-200"><td className="p-2">halls</td><td className="p-2">3.515 MHz</td><td className="p-2">bombs</td><td className="p-2">3.565 MHz</td></tr>
                    <tr className="border-b border-gray-200"><td className="p-2">slick</td><td className="p-2">3.522 MHz</td><td className="p-2">break</td><td className="p-2">3.572 MHz</td></tr>
                    <tr className="border-b border-gray-200"><td className="p-2">trick</td><td className="p-2">3.532 MHz</td><td className="p-2">brick</td><td className="p-2">3.575 MHz</td></tr>
                    <tr className="border-b border-gray-200"><td className="p-2">boxes</td><td className="p-2">3.535 MHz</td><td className="p-2">steak</td><td className="p-2">3.582 MHz</td></tr>
                    <tr className="border-b border-gray-200"><td className="p-2">leaks</td><td className="p-2">3.542 MHz</td><td className="p-2">sting</td><td className="p-2">3.592 MHz</td></tr>
                    <tr className="border-b border-gray-200"><td className="p-2">strobe</td><td className="p-2">3.545 MHz</td><td className="p-2">vector</td><td className="p-2">3.595 MHz</td></tr>
                    <tr><td className="p-2">bistro</td><td className="p-2">3.552 MHz</td><td className="p-2">beats</td><td className="p-2">3.600 MHz</td></tr>
                  </tbody>
                </table>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2">International Morse Code Chart:</h3>
                <div className="grid grid-cols-4 sm:grid-cols-6 gap-x-4 gap-y-1 text-sm">
                  <span>A: .-</span><span>B: -...</span><span>C: -.-.</span><span>D: -..</span><span>E: .</span><span>F: ..-.</span>
                  <span>G: --.</span><span>H: ....</span><span>I: ..</span><span>J: .---</span><span>K: -.-</span><span>L: .-..</span>
                  <span>M: --</span><span>N: -.</span><span>O: ---</span><span>P: .--.</span><span>Q: --.-</span><span>R: .-.</span>
                  <span>S: ...</span><span>T: -</span><span>U: ..-</span><span>V: ...-</span><span>W: .--</span><span>X: -..-</span>
                  <span>Y: -.--</span><span>Z: --..</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Wire Pulling Module Section */}
        <section id="wire-pulling">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Module: Wire Pulling
          </h2>
          <div className="space-y-4">
            <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 p-4" role="alert">
              <p className="font-bold">You only have one chance to successfully disarm this module.</p>
              <p>If you fail, you will not be able to try again.</p>
            </div>
            <p>
              This module presents 3 to 6 colored wires running vertically. To disarm it, one specific wire must be carefully pulled from its socket. Pulling the wrong wire will cause a strike. The wires must not be cut.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white space-y-4">
              <div>
                <h3 className="text-xl font-bold">If there are 3 wires:</h3>
                <ul className="list-disc list-inside mt-1">
                  <li>If there are no red wires, pull the second wire.</li>
                  <li>Otherwise, if the last wire is white, pull the last wire.</li>
                  <li>Otherwise, if there is more than one blue wire, pull the last blue wire.</li>
                  <li>Otherwise, pull the last wire.</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-bold">If there are 4 wires:</h3>
                <ul className="list-disc list-inside mt-1">
                  <li>If there is more than one red wire and the last digit of the serial number is odd, pull the last red wire.</li>
                  <li>Otherwise, if the last wire is yellow and there are no red wires, pull the first wire.</li>
                  <li>Otherwise, if there is exactly one blue wire, pull the first wire.</li>
                  <li>Otherwise, pull the second wire.</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-bold">If there are 5 wires:</h3>
                <ul className="list-disc list-inside mt-1">
                  <li>If the last wire is black and the last digit of the serial number is odd, pull the fourth wire.</li>
                  <li>Otherwise, if there is exactly one red wire and more than one yellow wire, pull the first wire.</li>
                  <li>Otherwise, if there are no black wires, pull the second wire.</li>
                  <li>Otherwise, pull the first wire.</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-bold">If there are 6 wires:</h3>
                <ul className="list-disc list-inside mt-1">
                  <li>If there are no yellow wires and the last digit of the serial number is odd, pull the third wire.</li>
                  <li>Otherwise, if there is exactly one yellow wire and more than one white wire, pull the fourth wire.</li>
                  <li>Otherwise, if there are no red wires, pull the last wire.</li>
                  <li>Otherwise, pull the fourth wire.</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Big Ass Button Module Section */}
        <section id="big-ass-button">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Module: Big Ass Button
          </h2>
          <div className="space-y-4">
            <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 p-4" role="alert">
              <p className="font-bold">This module can only be disarmed when all other modules (except needy ones) have been disarmed.</p>
              <p>Failure to adhere to this rule will result in detonation.</p>
            </div>
            <p>
              This module features a single, large button which contains an LED that can be lit. The button has no text on it. To disarm it, the button may need to be pressed and held. The timing of the release is critical and depends on whether the LED is lit and other bomb features.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white space-y-4">
              <h3 className="text-xl font-bold">Button Instructions:</h3>
              <p>Follow these rules in order. Perform the first action that applies based on the button&apos;s properties.</p>
              <ul className="list-disc list-inside space-y-2">
                <li>
                  If the LED is lit and there are more than 2 batteries, press and immediately release the button.
                </li>
                <li>
                  If the LED is off and there is more than 1 battery, hold the button. Refer to the &quot;Releasing a Held Button&quot; section.
                </li>
                <li>
                  If the LED is lit and the serial number contains a vowel, press and immediately release the button.
                </li>
                <li>
                  Otherwise, hold the button and refer to the &quot;Releasing a Held Button&quot; section.
                </li>
              </ul>
              <div className="p-4 border-t-2 border-gray-200">
                <h3 className="text-xl font-bold">Releasing a Held Button:</h3>
                <p>If you are holding the button, the display located at the centre of the bomb will light up. Release the button when the countdown timer has a specific digit in any position, according to the color of the big display:</p>
                <ul className="list-disc list-inside mt-2 space-y-1">
                  <li><span className="font-bold text-blue-600">Blue:</span> Release when timer has a <span className="font-bold">4</span>.</li>
                  <li><span className="font-bold text-yellow-500">Yellow:</span> Release when timer has a <span className="font-bold">5</span>.</li>
                  <li><span className="font-bold">Any other color:</span> Release when timer has a <span className="font-bold">1</span>.</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

      </main>

      <footer className="text-center mt-12 py-4 border-t-2 border-gray-300">
        <p className="text-sm text-gray-600">
          Manual Version 1.0.0 | Property of Defusal Corp.
        </p>
      </footer>
    </div>
  );
}
