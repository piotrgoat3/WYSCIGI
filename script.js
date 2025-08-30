document.addEventListener('DOMContentLoaded', () => {

    // --- Klasy Podstawowe ---

    class Zawodnik {
        constructor(imie, szybkosc, wytrzymalosc, refleks, taktyka, agresja) {
            this.imie = imie;
            this.szybkosc = szybkosc;
            this.wytrzymalosc = wytrzymalosc;
            this.refleks = refleks;
            this.taktyka = taktyka;
            this.agresja = agresja;
            this.forma = 80;
            this.zmeczenie = 0;
        }

        get overall() {
            return Math.round((this.szybkosc * 1.5 + this.wytrzymalosc + this.refleks + this.taktyka) / 4.5);
        }

        odpocznij() {
            this.zmeczenie = Math.max(0, this.zmeczenie - 30);
        }

        trenuj() {
            const stats = ['szybkosc', 'wytrzymalosc', 'refleks', 'taktyka'];
            const statToImprove = stats[Math.floor(Math.random() * stats.length)];
            if (this[statToImprove] < 100) {
                this[statToImprove]++;
            }
            this.zmeczenie = Math.min(100, this.zmeczenie + 10);
        }
    }

    class Druzyna {
        constructor(nazwa, zawodnicy = [], czyGracz = false) {
            this.nazwa = nazwa;
            this.zawodnicy = zawodnicy;
            this.punkty = 0;
            this.czyGracz = czyGracz;
        }
    }

    // --- Główny Obiekt Gry ---

    const LigaTorow = {
        druzyny: [],
        wolniZawodnicy: [],
        druzynaGracza: null,
        dzien: 1,
        reputacja: 50,

        init(nazwaDruzynyGracza) {
            // Generowanie drużyny gracza
            const zawodnicyGracza = Array.from({ length: 4 }, () => this.generujZawodnika(50, 65));
            this.druzynaGracza = new Druzyna(nazwaDruzynyGracza, zawodnicyGracza, true);
            this.druzyny.push(this.druzynaGracza);

            // Generowanie drużyn AI
            const nazwyAI = ["Stalowe Tłoki", "Nocne Jastrzębie", "Tytani Prędkości"];
            nazwyAI.forEach(nazwa => {
                const zawodnicyAI = Array.from({ length: 4 }, () => this.generujZawodnika(50, 70));
                this.druzyny.push(new Druzyna(nazwa, zawodnicyAI));
            });

            // Generowanie wolnych zawodników
            this.wolniZawodnicy = Array.from({ length: 10 }, () => this.generujZawodnika(40, 75));
            
            this.updateUI();
        },

        generujZawodnika(min, max) {
            const imiona = ["Jan", "Piotr", "Adam", "Kamil", "Marek", "Łukasz"];
            const nazwiska = ["Kowalski", "Nowak", "Wiśniewski", "Wójcik", "Lis"];
            const imie = `${imiona[Math.floor(Math.random() * imiona.length)]} ${nazwiska[Math.floor(Math.random() * nazwiska.length)]}`;
            
            const losujStat = () => Math.floor(Math.random() * (max - min + 1)) + min;
            return new Zawodnik(imie, losujStat(), losujStat(), losujStat(), losujStat(), losujStat());
        },
        
        symulujWyscig(skladGracza) {
            let uczestnicy = [...skladGracza];
            // AI wybiera skład
            this.druzyny.forEach(d => {
                if (!d.czyGracz) {
                    const skladAI = [...d.zawodnicy].sort((a,b) => (b.forma - b.zmeczenie) - (a.forma - a.zmeczenie)).slice(0, 3);
                    uczestnicy.push(...skladAI);
                }
            });

            const wyniki = uczestnicy.map(zawodnik => {
                const mocBazowa = (zawodnik.szybkosc * 1.2 + zawodnik.wytrzymalosc + zawodnik.refleks + zawodnik.taktyka);
                const mocZForma = mocBazowa * (zawodnik.forma / 100);
                const bonusAgresji = (zawodnik.agresja / 10) * (Math.random() * 1.5);
                const losowosc = Math.random() * 30 - 15;
                const finalnyWynik = Math.round(mocZForma + bonusAgresji + losowosc);

                zawodnik.zmeczenie = Math.min(100, zawodnik.zmeczenie + Math.floor(Math.random() * 15) + 20);
                return { zawodnik, wynik: finalnyWynik };
            }).sort((a, b) => b.wynik - a.wynik);

            const punktyDoZdobycia = [10, 8, 6, 4, 2, 1];
            wyniki.forEach((res, i) => {
                const druzynaZawodnika = this.druzyny.find(d => d.zawodnicy.includes(res.zawodnik));
                if (i < punktyDoZdobycia.length) {
                    druzynaZawodnika.punkty += punktyDoZdobycia[i];
                    res.zawodnik.forma = Math.min(100, res.zawodnik.forma + 10 - i);
                } else {
                    res.zawodnik.forma = Math.max(0, res.zawodnik.forma - 5);
                }
            });
            this.dzien++;
            return wyniki;
        },

        // --- Metody do renderowania UI ---
        
        updateUI() {
            document.getElementById('player-team-name').textContent = this.druzynaGracza.nazwa;
            document.getElementById('game-stats').textContent = `Dzień: ${this.dzien} | Reputacja: ${this.reputacja}`;
            this.renderClubView(); // Domyślny widok
        },

        clearContent() {
            document.getElementById('game-content').innerHTML = '';
        },

        renderClubView() {
            this.clearContent();
            const content = document.getElementById('game-content');
            const container = document.createElement('div');
            container.className = 'view-container';
            container.innerHTML = `<h2>Zarządzanie Składem</h2>`;

            this.druzynaGracza.zawodnicy.forEach((z, index) => {
                const card = document.createElement('div');
                card.className = 'player-card';
                card.innerHTML = `
                    <div class="info"><strong>${z.imie}</strong> (Overall: ${z.overall})</div>
                    <div class="stats">
                        <span>Szyb: ${z.szybkosc}</span>
                        <span>Wytrz: ${z.wytrzymalosc}</span>
                        <span>Refl: ${z.refleks}</span>
                        <span>Takt: ${z.taktyka}</span>
                        <span>Forma: ${z.forma}%</span>
                        <span>Zmęcz: ${z.zmeczenie}%</span>
                    </div>
                    <div class="actions">
                        <button class="train-btn" data-index="${index}">Trenuj</button>
                        <button class="rest-btn" data-index="${index}">Odpocznij</button>
                    </div>
                `;
                container.appendChild(card);
            });
            content.appendChild(container);
        },
        
        renderMarketView() {
            this.clearContent();
            const content = document.getElementById('game-content');
            const container = document.createElement('div');
            container.className = 'view-container';
            container.innerHTML = `<h2>Wolni Zawodnicy</h2>`;
            
            this.wolniZawodnicy.forEach((z, index) => {
                const card = document.createElement('div');
                card.className = 'player-card';
                card.innerHTML = `
                    <div class="info"><strong>${z.imie}</strong> (Overall: ${z.overall})</div>
                    <div class="stats">
                        <span>Szyb: ${z.szybkosc}</span>
                        <span>Wytrz: ${z.wytrzymalosc}</span>
                        <span>Refl: ${z.refleks}</span>
                        <span>Takt: ${z.taktyka}</span>
                    </div>
                    <div class="actions">
                        <button class="sign-btn" data-index="${index}">Kontraktuj</button>
                    </div>
                `;
                container.appendChild(card);
            });
            content.appendChild(container);
        },
        
        renderLeagueTableView() {
            this.clearContent();
            const content = document.getElementById('game-content');
            const container = document.createElement('div');
            container.className = 'view-container';
            container.innerHTML = `<h2>Tabela Ligi</h2>`;
            
            const table = document.createElement('ol');
            table.id = 'league-table';
            
            const posortowaneDruzyny = [...this.druzyny].sort((a,b) => b.punkty - a.punkty);
            posortowaneDruzyny.forEach(d => {
                const row = document.createElement('li');
                row.innerHTML = `<strong>${d.nazwa}</strong> - ${d.punkty} pkt. ${d.czyGracz ? '(Ty)' : ''}`;
                table.appendChild(row);
            });
            
            container.appendChild(table);
            content.appendChild(container);
        },

        renderRaceSelection() {
            this.clearContent();
            const content = document.getElementById('game-content');
            const container = document.createElement('div');
            container.className = 'view-container';
            container.innerHTML = `<h2>Wybierz 3 zawodników na wyścig</h2>`;
            
            this.druzynaGracza.zawodnicy.forEach((z, index) => {
                const label = document.createElement('label');
                label.className = 'race-selection-label';
                label.innerHTML = `<input type="checkbox" class="race-checkbox" value="${index}"> ${z.imie} (Overall: ${z.overall}, Forma: ${z.forma}%, Zmęcz: ${z.zmeczenie}%)`;
                container.appendChild(label);
            });

            const startButton = document.createElement('button');
            startButton.textContent = 'Start Wyścigu!';
            startButton.className = 'menu-btn race-btn';
            startButton.style.marginTop = '20px';
            startButton.onclick = () => {
                const selectedCheckboxes = document.querySelectorAll('.race-checkbox:checked');
                if (selectedCheckboxes.length !== 3) {
                    alert('Musisz wybrać dokładnie 3 zawodników!');
                    return;
                }
                const sklad = Array.from(selectedCheckboxes).map(cb => this.druzynaGracza.zawodnicy[cb.value]);
                const wyniki = this.symulujWyscig(sklad);
                this.renderRaceResults(wyniki);
            };
            container.appendChild(startButton);
            content.appendChild(container);
        },
        
        renderRaceResults(wyniki) {
            this.clearContent();
            const content = document.getElementById('game-content');
            const container = document.createElement('div');
            container.className = 'view-container';
            container.innerHTML = `<h2>Wyniki Wyścigu (Dzień ${this.dzien - 1})</h2>`;

            const list = document.createElement('ol');
            list.id = 'race-results-list';
            wyniki.forEach(res => {
                const druzyna = this.druzyny.find(d => d.zawodnicy.includes(res.zawodnik));
                const item = document.createElement('li');
                item.innerHTML = `<strong>${res.zawodnik.imie}</strong> (${druzyna.nazwa}) - Wynik: ${res.wynik}`;
                list.appendChild(item);
            });
            container.appendChild(list);

            const nextButton = document.createElement('button');
            nextButton.textContent = 'Przejdź do następnego dnia';
            nextButton.className = 'menu-btn';
            nextButton.style.marginTop = '20px';
            nextButton.onclick = () => {
                document.getElementById('show-club-btn').click();
                this.updateUI();
            };
            container.appendChild(nextButton);

            content.appendChild(container);
        }
    };

    // --- Obsługa Zdarzeń ---

    const setupScreen = document.getElementById('setup-screen');
    const mainScreen = document.getElementById('main-screen');
    
    document.getElementById('start-game-btn').addEventListener('click', () => {
        const teamName = document.getElementById('team-name-input').value;
        if (teamName.trim() === '') {
            alert('Nazwa drużyny nie może być pusta!');
            return;
        }
        setupScreen.classList.add('hidden');
        mainScreen.classList.remove('hidden');
        LigaTorow.init(teamName);
    });

    // Nawigacja
    const menuButtons = document.querySelectorAll('.menu-btn');
    menuButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            menuButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    document.getElementById('show-club-btn').addEventListener('click', () => LigaTorow.renderClubView());
    document.getElementById('show-market-btn').addEventListener('click', () => LigaTorow.renderMarketView());
    document.getElementById('show-league-btn').addEventListener('click', () => LigaTorow.renderLeagueTableView());
    document.getElementById('show-race-btn').addEventListener('click', () => LigaTorow.renderRaceSelection());
    
    // Delegacja zdarzeń dla akcji na zawodnikach
    document.getElementById('game-content').addEventListener('click', (e) => {
        const index = e.target.dataset.index;
        if (index === undefined) return;

        if (e.target.classList.contains('train-btn')) {
            LigaTorow.druzynaGracza.zawodnicy[index].trenuj();
            LigaTorow.renderClubView();
        } else if (e.target.classList.contains('rest-btn')) {
            LigaTorow.druzynaGracza.zawodnicy[index].odpocznij();
            LigaTorow.renderClubView();
        } else if (e.target.classList.contains('sign-btn')) {
            if (LigaTorow.druzynaGracza.zawodnicy.length >= 6) {
                alert("Masz już maksymalną liczbę zawodników!");
                return;
            }
            const zawodnik = LigaTorow.wolniZawodnicy.splice(index, 1)[0];
            LigaTorow.druzynaGracza.zawodnicy.push(zawodnik);
            LigaTorow.renderMarketView();
        }
    });
});
