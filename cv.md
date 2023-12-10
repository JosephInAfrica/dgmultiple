# CV

### JiaJun Li  [lochlee@yahoo.com](mailto:lochlee@yahoo.com)

### Education:

### 2009-2013 Qingdao University, Major in Chemistry, Bachelor degree

### *Backend Developer*

***Oppo Mobile Telecommunications Corp.**, Shenzhen, China – (Oct 2020 - Present)*

- backend developer in **Host-based intrusion detection system(HIDS)** team, major in Go language,
- developed and maintained the backend service for shielding Android applications against reverse engineering. Integrated this service into the internal CI/CD system, which is currently used as infrastructure.
- contributed to the design and implementation of backend service of **host-based intrusion detection system** (HIDS), which is protecting 100k servers in real-time internally
- in charge of backend service for the company's **Security Operations Center** **(SOC)**,migrated it from Java to Go and continuously adding features to it.

***Digitalor Technology Company Ltd.**, Shenzhen, China – (Mar 2019 - Oct 2020)*

- built Linux Programs running on the company's controller products using Python and Go
- designed and implemented backend service managing state and tasks of sensors, which makes developing service much easier .

***China Progress Freight Forwarding Com. Ltd.** ,Shenzhen,China - (March 2017--Feb 2019)*

- maintained and added features to the web crawler system
- developed and maintained internal logistics inquiry service

 ***Bedmate Furniture International**, Lagos, Nigeria – (Mar 2019 - Oct 2020)*

- maintained PCs and Networks infrastructure of the company;
- administered importing, and customs clearance affairs

### 

Core courses: Calculus, Linear Algebra, **Probability theory**, Language C

### Skills:

- **Chinese**: Native Speaker
- **English**: Fluent in English communication,2 years working in an English environment(Nigeria),
- **Programming Language**: Go, Python,Javascript, Rust
- **Frontend Frameworks**: Vue.js
- **Database**: MySQL,MongoDB,Redis, Kafka

### Projects Experience

- hids backend:
    - // shall I explain what does it do?  a serving
        - contributed solely on messaging between agent and backend: tasks dispatch and ,  heartbeat, status management in  groups, and so on.
        - 
1. 天蝎
2. soc
3. Program for MiniBox(An embedded hardware that runs linux, product of Shenzhen Digitalor Company):
- Introduction: The program runs on embedded Linux [system.It](http://system.it/) collects info from attached devices (through RS485),and serves the client with HTTP connections.I did all designing and programming work on my own.
- Modules:
    - **I/O interface with devices connected through RS485(serial Port)**:
    The program Interact constantly through serial port with connected devices ,gathering info from them and sending commands to them.
    - **Datacenter**
    Datacenter module receives info from I/O interface ,treats and caches it, and is always ready to serve it through Api and Web.
    - **Api and Web**
    Api and web are interfaces connecting clients and the program. They supplies client with info from Datacenter, and despatch commands from client to attached devices through I/O interface. Api and Web backend is built with Python/Tornado.Web front end is built with Vue.js.
- Summary:
    - This Program applies multi-threading design pattern. I/O interface and Api/web run in parallel, while interacting with each other through Datacenter.
    - Tornado serve api/web backend asynchronously using coroutines. Both Api and web run fluently and steadily.
    - The device carrying this program is competing to be part of Tencent's infrastructure products.